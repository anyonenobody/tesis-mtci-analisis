#!/usr/bin/env python3
"""
Motor Autónomo de Búsqueda y Aprendizaje Iterativo para Revisiones PRISMA-ScR.
Ejecuta ciclos sucesivos de búsqueda multi-API, evalúa precisión semántica,
aprende nuevos descriptores de alto rendimiento y purga ruido temático.
"""

import sys
import os
import argparse
import json
import re
from collections import Counter
from datetime import date
from typing import List, Dict, Any, Set

# Asegurar salida UTF-8 en terminales Windows
try:
    if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    if sys.stderr.encoding and sys.stderr.encoding.lower() != 'utf-8':
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# Asegurar acceso a los módulos del proyecto (local o fallback a prisma-scr para ejecución global multi-proyecto)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
PRISMA_SCR_FALLBACK = r"c:\Users\fungicoder\Documents\Fungicoder\Dev\prisma-scr"

HAS_LOCAL_CORE = os.path.exists(os.path.join(os.getcwd(), "core", "api_fetcher.py"))
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())
if PROJECT_ROOT not in sys.path and os.path.exists(os.path.join(PROJECT_ROOT, "core", "api_fetcher.py")):
    sys.path.insert(0, PROJECT_ROOT)
    HAS_LOCAL_CORE = True
elif os.path.exists(PRISMA_SCR_FALLBACK) and PRISMA_SCR_FALLBACK not in sys.path:
    sys.path.append(PRISMA_SCR_FALLBACK)

from core.api_fetcher import (
    search_openalex_api,
    search_pubmed_api,
    search_crossref_api,
    search_europe_pmc_api,
    smart_relevance_score,
    federated_multi_api_search
)
if HAS_LOCAL_CORE:
    from core.storage import (
        get_connection,
        insert_articles,
        add_search_log,
        run_deduplication,
        export_project_snapshot,
        get_articles
    )
else:
    def get_articles(include_duplicates: bool = True) -> List[Dict[str, Any]]:
        return []

# Palabras vacías en español, portugués e inglés para minería de términos
STOPWORDS = {
    "de", "la", "el", "en", "y", "a", "los", "del", "las", "con", "un", "para", "por",
    "una", "su", "al", "lo", "como", "mas", "más", "pero", "sus", "le", "ya", "o", "fue",
    "este", "ha", "si", "sobre", "entre", "cuando", "muy", "sin", "sobre", "tambien", "también",
    "the", "of", "and", "in", "to", "a", "with", "for", "is", "on", "that", "by", "this",
    "as", "an", "are", "from", "at", "it", "was", "were", "or", "be", "study", "results",
    "dos", "das", "em", "um", "uma", "com", "nao", "não", "para", "por", "que", "estudo"
}

NOISE_SIGNALS = [
    "in vitro", "cell line", "antimicrobial", "antifungal", "candida", "antibacterial",
    "mice", "rats", "murine", "agronomic", "soil", "fungicide", "veterinary", "bovine"
]


class IterativeSearchEngine:
    """Motor de búsqueda con ciclo de realimentación y auto-mejora."""

    def __init__(self, target_api: str = "openalex", max_iterations: int = 3, target_yield: int = 15):
        self.target_api = target_api.lower()
        self.max_iterations = max_iterations
        self.target_yield = target_yield
        self.discovered_dois: Set[str] = set()
        self.learned_keywords: Set[str] = set()
        self.negative_filters: Set[str] = set()
        self.trajectory_log: List[Dict[str, Any]] = []

        # Cargar DOIs ya presentes en la base de datos
        existing = get_articles(include_duplicates=True)
        for a in existing:
            doi = (a.get("doi") or "").strip().lower()
            if doi:
                self.discovered_dois.add(doi)

    def fetch_api(self, query: str, limit: int = 25) -> List[Dict[str, Any]]:
        """Llama a la API seleccionada o ejecuta el pipeline federado multi-API en paralelo."""
        if self.target_api in ["federated", "all"]:
            fed = federated_multi_api_search(
                query=query,
                apis=["openalex", "pubmed", "crossref", "europe_pmc"],
                max_results_per_api=max(limit // 2, 15)
            )
            self.last_federated_metrics = fed.get("metrics", {})
            return fed.get("records", [])
        elif "openalex" in self.target_api:
            return search_openalex_api(query, max_results=limit)
        elif "pubmed" in self.target_api:
            return search_pubmed_api(query, max_results=limit)
        elif "crossref" in self.target_api:
            return search_crossref_api(query, max_results=limit)
        elif "europe" in self.target_api:
            return search_europe_pmc_api(query, max_results=limit)
        else:
            return search_openalex_api(query, max_results=limit)

    def analyze_and_learn(self, articles: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analiza los resultados:
        1. Separa por categoría de relevancia (Alta, Parcial, Baja).
        2. Extrae términos candidatos que aparecen con alta frecuencia en artículos de alta relevancia.
        3. Detecta señales de ruido somático o biológico para auto-inclusión en filtros negativos.
        """
        high_rel = []
        low_rel = []
        words_in_high = []

        for art in articles:
            score = smart_relevance_score(art.get("title", ""), art.get("abstract", ""))
            art["score_info"] = score
            label = score.get("status_label", "")

            if label.startswith("Alta"):
                high_rel.append(art)
                text = f"{art.get('title', '')} {art.get('abstract', '')}".lower()
                tokens = re.findall(r"\b[a-záéíóúñ]{4,18}\b", text)
                filtered = [t for t in tokens if t not in STOPWORDS]
                words_in_high.extend(filtered)
            elif label.startswith("Baja"):
                low_rel.append(art)
                text = f"{art.get('title', '')} {art.get('abstract', '')}".lower()
                for ns in NOISE_SIGNALS:
                    if ns in text:
                        self.negative_filters.add(ns)

        # Minería de palabras clave frecuentes en artículos de alta relevancia
        term_freq = Counter(words_in_high).most_common(12)
        candidate_terms = [t for t, count in term_freq if count >= 2]

        precision = len(high_rel) / len(articles) if articles else 0.0

        return {
            "total": len(articles),
            "high_count": len(high_rel),
            "low_count": len(low_rel),
            "precision": precision,
            "high_articles": high_rel,
            "learned_candidate_terms": candidate_terms
        }

    def build_refined_query(self, base_concept: str, iteration: int) -> str:
        """Construye una ecuación booleana auto-mejorada para la siguiente iteración."""
        query = base_concept

        # Incorporar nuevos términos aprendidos de alto valor
        if self.learned_keywords:
            top_learned = list(self.learned_keywords)[:4]
            learned_block = " OR ".join([f'"{kw}"' for kw in top_learned])
            query = f"({query}) AND ({learned_block})"

        # Incorporar filtros de exclusión si se detectó ruido
        if self.negative_filters:
            neg_terms = list(self.negative_filters)[:3]
            not_block = " NOT (" + " OR ".join([f'"{nt}"' for nt in neg_terms]) + ")"
            query += not_block

        return query

    def run_loop(self, initial_query: str, auto_import: bool = True) -> Dict[str, Any]:
        """Ejecuta el ciclo de investigación iterativa completa."""
        current_query = initial_query
        cumulative_high_articles = []
        iteration_stats = []

        print(f"\n=======================================================")
        print(f"🚀 INICIANDO CICLO DE INVESTIGACIÓN ITERATIVA PRISMA-ScR")
        print(f"API Objetivo: {self.target_api.upper()} | Meta: {self.target_yield} estudios de alta relevancia")
        print(f"=======================================================\n")

        for it in range(1, self.max_iterations + 1):
            print(f"--- [Iteración {it}/{self.max_iterations}] ---")
            print(f"Ecuación empleada: {current_query}")

            fetched = self.fetch_api(current_query, limit=self.target_yield * 2)
            if not fetched:
                print("⚠️ No se recuperaron registros en esta iteración. Ajustando amplitud...")
                break

            analysis = self.analyze_and_learn(fetched)
            precision_pct = round(analysis["precision"] * 100, 1)

            print(f"Recuperados: {analysis['total']} | Alta relevancia: {analysis['high_count']} | Precisión: {precision_pct}%")

            # Filtrar novedades (no duplicadas con iteraciones previas o DB)
            new_high = []
            for art in analysis["high_articles"]:
                doi = (art.get("doi") or "").strip().lower()
                title_clean = art.get("title", "").strip().lower()
                if doi and doi in self.discovered_dois:
                    continue
                if any(title_clean == a.get("title", "").strip().lower() for a in cumulative_high_articles):
                    continue

                new_high.append(art)
                if doi:
                    self.discovered_dois.add(doi)

            cumulative_high_articles.extend(new_high)
            print(f"Nuevos estudios descubiertos y retenidos en esta iteración: {len(new_high)}")

            # Realimentación: actualizar términos aprendidos
            for t in analysis["learned_candidate_terms"]:
                if len(t) > 4:
                    self.learned_keywords.add(t)

            iteration_stats.append({
                "iteration": it,
                "query": current_query,
                "retrieved": analysis["total"],
                "high_count": analysis["high_count"],
                "new_retained": len(new_high),
                "precision": precision_pct,
                "learned_terms": list(self.learned_keywords)
            })

            # Condición de parada anticipada: cuota satisfecha
            if len(cumulative_high_articles) >= self.target_yield:
                print(f"🎯 Meta alcanzada: {len(cumulative_high_articles)} estudios de alta pertinencia acumulados.")
                break

            # Refinar ecuación para la próxima iteración
            current_query = self.build_refined_query(initial_query, it)

        # Ingestión automática en la base de datos si se solicitó y existe core.storage local
        imported_count = 0
        if auto_import and HAS_LOCAL_CORE and cumulative_high_articles:
            imported_count = insert_articles(cumulative_high_articles)
            if self.target_api in ["federated", "all"] and hasattr(self, "last_federated_metrics"):
                stats_map = self.last_federated_metrics.get("sources_stats", {})
                for sk, sv in stats_map.items():
                    add_search_log(
                        database_name=sv["name"],
                        search_string=initial_query,
                        results_count=sv["count"],
                        search_date=str(date.today()),
                        notes=f"Descubrimiento iterativo concurrente ({sv['latency_ms']} ms)"
                    )
            else:
                add_search_log(
                    database_name=f"{self.target_api.capitalize()} (Iterative Search)",
                    search_string=initial_query,
                    results_count=len(cumulative_high_articles),
                    search_date=str(date.today()),
                    notes=f"Descubrimiento iterativo autónomo: {len(cumulative_high_articles)} artículos de alta relevancia"
                )
            run_deduplication(title_similarity_threshold=90.0)
            export_project_snapshot()
            print(f"💾 {imported_count} artículos insertados en SQLite y snapshot exportado con éxito.")
        elif auto_import and not HAS_LOCAL_CORE and cumulative_high_articles:
            print("ℹ️ Ejecución en modo autónomo multi-proyecto (sin base SQLite local): resultados incluidos en el reporte JSON.")

        summary = {
            "api": self.target_api,
            "total_iterations_run": len(iteration_stats),
            "total_high_yield_found": len(cumulative_high_articles),
            "imported_to_db": imported_count,
            "iterations_detail": iteration_stats,
            "learned_vocabulary": list(self.learned_keywords),
            "negative_filters_applied": list(self.negative_filters),
            "articles": [
                {
                    "title": a.get("title"),
                    "authors": a.get("authors"),
                    "year": a.get("year"),
                    "journal": a.get("journal"),
                    "doi": a.get("doi"),
                    "source_db": a.get("source_db"),
                }
                for a in cumulative_high_articles
            ]
        }

        return summary


def main():
    parser = argparse.ArgumentParser(description="Ejecutor de Búsqueda Iterativa PRISMA-ScR")
    parser.add_argument(
        "--api",
        default="federated",
        choices=["federated", "all", "openalex", "pubmed", "crossref", "europe"],
        help="Servicio API (o 'federated' para consultar todas concurrentemente en paralelo)"
    )
    parser.add_argument("--query", required=True, help="Ecuación base o concepto a investigar")
    parser.add_argument("--iterations", type=int, default=3, help="Número máximo de ciclos iterativos")
    parser.add_argument("--target", type=int, default=10, help="Meta de artículos de alta relevancia")
    parser.add_argument("--no-import", action="store_true", help="Solo auditar sin insertar en la base de datos")

    args = parser.parse_args()

    engine = IterativeSearchEngine(target_api=args.api, max_iterations=args.iterations, target_yield=args.target)
    result = engine.run_loop(initial_query=args.query, auto_import=(not args.no_import))

    print("\n================== REPORTE DE RESULTADOS ==================")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
