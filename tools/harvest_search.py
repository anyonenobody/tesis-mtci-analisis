#!/usr/bin/env python3
"""
Autonomous Multi-API Harvesting Engine for PRISMA-ScR Scoping Reviews.
Executes systematic Phase 1 (MeSH/DeCS Umbrella) and Phase 2 (Granular Modalities & Clinical Triad)
searches across PubMed, Europe PMC, OpenAlex, and Crossref APIs.
Enforces trilingual coverage (ES, EN, PT), 21 Latin American countries, and 2016-2026 temporal limits.
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import Dict, Any, List

# Reconfigure stdout/stderr for Unicode/UTF-8 on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Ensure repository root is on sys.path
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)
PRISMA_SCR_FALLBACK = r"c:\Users\fungicoder\Documents\Fungicoder\Dev\prisma-scr"
if os.path.exists(PRISMA_SCR_FALLBACK) and PRISMA_SCR_FALLBACK not in sys.path:
    sys.path.append(PRISMA_SCR_FALLBACK)

from core.pcc_data import (
    PHASE1_UMBRELLA_TAXONOMY,
    PHASE2_GRANULAR_MTCI,
    PHASE2_PSYCH_DOMAINS,
    LATAM_COUNTRIES_METADATA,
    TEMPORAL_WINDOW
)
from core.api_fetcher import (
    search_openalex_api,
    search_pubmed_api,
    search_europe_pmc_api,
    search_crossref_api,
    smart_relevance_score
)
from core.storage import (
    insert_articles,
    add_search_log,
    run_deduplication,
    get_articles,
    get_prisma_flow_numbers,
    export_project_snapshot
)


def build_phase1_queries(languages: List[str] = ["es", "en", "pt"]) -> List[Dict[str, str]]:
    """Genera las ecuaciones de búsqueda para la Fase 1 (Concepto Paraguas MeSH / DeCS)."""
    queries = []
    
    # Bloque MTCI paraguas en los idiomas seleccionados
    umbrella_terms = []
    for lang in languages:
        umbrella_terms.extend(PHASE1_UMBRELLA_TAXONOMY.get(lang, []))
    
    # Términos paraguas más compactos y representativos para APIs
    mtci_es = '("medicina tradicional" OR "terapias complementarias" OR "medicina integrativa")'
    mtci_en = '("traditional medicine" OR "complementary therapies" OR "integrative medicine")'
    mtci_pt = '("práticas integrativas" OR "PICS" OR "terapias complementares")'
    
    psych_core = '("psicologia" OR "psicoterapia" OR "salud mental" OR "psychotherapy" OR "mental health" OR "saude mental")'
    latam_core = '("America Latina" OR "Latin America" OR "Brasil" OR "Mexico" OR "Colombia" OR "Chile" OR "Nicaragua" OR "Peru" OR "Argentina")'

    # Ecuación balanceada en inglés/multilingüe para APIs internacionales
    queries.append({
        "label": "Fase 1 MeSH/DeCS - MTCI Paraguas Multilingüe",
        "phase": "1",
        "query": f'({mtci_en} OR {mtci_es} OR {mtci_pt}) AND {psych_core} AND {latam_core}'
    })

    # Ecuación específica en portugués (PICS / SUS / Brasil)
    if "pt" in languages:
        queries.append({
            "label": "Fase 1 MeSH/DeCS - PICS & Atenção Psicossocial (Brasil/SUS)",
            "phase": "1",
            "query": '("praticas integrativas" OR "PICS" OR "terapias complementares") AND ("saude mental" OR "atencao psicossocial" OR "psicologia") AND ("Brasil" OR "SUS")'
        })

    # Ecuación específica en español (Medicina Tradicional e Integrativa / Salud Mental LatAm)
    if "es" in languages:
        queries.append({
            "label": "Fase 1 MeSH/DeCS - MTCI & Psicología (Hispanoamérica)",
            "phase": "1",
            "query": '("medicina tradicional" OR "medicina integrativa" OR "terapias complementarias") AND ("psicoterapia" OR "salud mental" OR "intervencion psicologica") AND ("America Latina" OR "Colombia" OR "Mexico" OR "Chile" OR "Nicaragua")'
        })

    return queries


def build_phase2_queries(languages: List[str] = ["es", "en", "pt"]) -> List[Dict[str, str]]:
    """Genera las ecuaciones de búsqueda para la Fase 2 (Prácticas Específicas & Tríada Psicológica)."""
    queries = []

    # 1. Fitoterapia & Plantas Medicinales
    queries.append({
        "label": "Fase 2 Granular - Fitoterapia & Plantas Medicinales en Salud Mental",
        "phase": "2",
        "modality": "Fitoterapia",
        "query": '("phytotherapy" OR "medicinal plants" OR "fitoterapia" OR "plantas medicinais") AND ("anxiety" OR "depression" OR "ansiedad" OR "depressao" OR "insomnia") AND ("Latin America" OR "Brazil" OR "Mexico" OR "Colombia" OR "Nicaragua")'
    })

    # 2. Acupuntura & Auriculoterapia
    queries.append({
        "label": "Fase 2 Granular - Acupuntura & Auriculoterapia en Psicoterapia/Salud Mental",
        "phase": "2",
        "modality": "Acupuntura",
        "query": '("acupuncture" OR "auriculotherapy" OR "acupuntura" OR "auriculoterapia") AND ("psychotherapy" OR "depression" OR "anxiety" OR "ansiedad" OR "depresion" OR "stress") AND ("Latin America" OR "Brazil" OR "Colombia" OR "Mexico" OR "Chile")'
    })

    # 3. Mindfulness & Terapias Mente-Cuerpo / Yoga
    queries.append({
        "label": "Fase 2 Granular - Mindfulness, Yoga & Técnicas Contemplativas",
        "phase": "2",
        "modality": "Mindfulness",
        "query": '("mindfulness" OR "meditation" OR "yoga" OR "atencion plena" OR "ioga") AND ("psychotherapy" OR "CBT" OR "TCC" OR "stress" OR "burnout" OR "depression") AND ("Latin America" OR "Brazil" OR "Mexico" OR "Chile" OR "Colombia")'
    })

    # 4. Saberes Ancestrales & Medicina Tradicional Indígena
    queries.append({
        "label": "Fase 2 Granular - Saberes Ancestrales, Medicina Indígena & Ayahuasca",
        "phase": "2",
        "modality": "Saberes Ancestrales",
        "query": '("ancestral knowledge" OR "indigenous medicine" OR "ayahuasca" OR "shamanism" OR "saberes ancestrales" OR "pajelanca") AND ("mental health" OR "psychotherapy" OR "trauma" OR "depression" OR "saude mental") AND ("Latin America" OR "Brazil" OR "Colombia" OR "Peru")'
    })

    # 5. Terapias Florales & Bioenergéticas
    queries.append({
        "label": "Fase 2 Granular - Terapias Florales & Bioenergéticas (Bach, Reiki)",
        "phase": "2",
        "modality": "Terapias Florales",
        "query": '("flower essences" OR "flower therapy" OR "reiki" OR "florais de bach" OR "terapia floral") AND ("psychotherapy" OR "anxiety" OR "stress" OR "ansiedade" OR "grief" OR "duelo") AND ("Latin America" OR "Brazil" OR "Chile" OR "Mexico" OR "Colombia")'
    })

    # 6. Terapias Artísticas & Corporales Integrativas
    queries.append({
        "label": "Fase 2 Granular - Arteterapia & Biodanza Integrativa en Salud Mental",
        "phase": "2",
        "modality": "Terapias Artísticas",
        "query": '("art therapy" OR "music therapy" OR "biodanza" OR "arteterapia" OR "biodanca") AND ("mental health" OR "psychotherapy" OR "saude mental" OR "atencao psicossocial") AND ("Latin America" OR "Brazil" OR "Argentina" OR "Colombia" OR "Chile")'
    })

    return queries


def execute_harvest(
    phases: List[str] = ["1", "2"],
    apis: List[str] = ["openalex", "europe_pmc", "pubmed", "crossref"],
    max_per_query_api: int = 25,
    auto_dedup: bool = True,
    auto_prescreen: bool = True
) -> Dict[str, Any]:
    """Ejecuta la cosecha sistemática federada de artículos según las fases especificadas."""
    print("=" * 70)
    print("🌿 INICIANDO COSECHA SISTEMÁTICA AUTOMATIZADA PRISMA-ScR")
    print(f"Fases: {phases} | APIs: {apis} | Límite por consulta/API: {max_per_query_api}")
    print(f"Ventana Temporal: {TEMPORAL_WINDOW['label']}")
    print("=" * 70)

    query_plan = []
    if "1" in phases or "both" in phases or "all" in phases:
        query_plan.extend(build_phase1_queries())
    if "2" in phases or "both" in phases or "all" in phases:
        query_plan.extend(build_phase2_queries())

    api_functions = {
        "openalex": ("OpenAlex API", search_openalex_api),
        "europe_pmc": ("Europe PMC API", search_europe_pmc_api),
        "pubmed": ("PubMed API", search_pubmed_api),
        "crossref": ("Crossref API", search_crossref_api)
    }

    selected_api_functions = {k: v for k, v in api_functions.items() if k in apis}

    total_harvested_raw = 0
    records_by_api = {k: 0 for k in selected_api_functions.keys()}
    all_new_articles = []
    today_str = datetime.now().strftime("%Y-%m-%d")

    for idx, q_info in enumerate(query_plan, start=1):
        label = q_info["label"]
        q_str = q_info["query"]
        print(f"\n[{idx}/{len(query_plan)}] Ejecutando consulta: {label}")
        print(f"  Sintaxis: {q_str[:85]}...")

        query_total = 0
        for api_key, (api_name, search_fn) in selected_api_functions.items():
            try:
                t0 = time.time()
                results = search_fn(q_str, max_results=max_per_query_api)
                elapsed = time.time() - t0
                n_res = len(results)
                records_by_api[api_key] += n_res
                query_total += n_res
                print(f"    • {api_name}: {n_res} registros ({elapsed:.2f}s)")

                # Registrar en logs de búsqueda para trazabilidad PRISMA
                add_search_log(
                    database_name=api_name,
                    search_string=q_str,
                    results_count=n_res,
                    search_date=today_str,
                    notes=f"{label} [Fase {q_info.get('phase', '1')}]"
                )

                all_new_articles.extend(results)

            except Exception as ex:
                print(f"    ❌ Error en {api_name}: {ex}")

        total_harvested_raw += query_total
        print(f"  Subtotal de la consulta: {query_total} registros.")

    # Inserción en la base de datos SQLite
    print("\n" + "-" * 70)
    print(f"💾 Insertando {len(all_new_articles)} registros brutos en SQLite...")
    inserted_count = insert_articles(all_new_articles)
    print(f"✅ Artículos insertados con éxito: {inserted_count}")

    # Deduplicación automática
    dedup_results = {}
    if auto_dedup:
        print("\n🔍 Ejecutando Deduplicación Híbrida (DOI + RapidFuzz Token Sort Ratio 90%)...")
        dedup_results = run_deduplication(title_similarity_threshold=90.0)
        print(f"✅ Duplicados identificados y marcados: {dedup_results.get('duplicates_found', 0)}")

    # Triaje / Prescreening algorítmico inteligente
    prescreen_results = {}
    if auto_prescreen:
        print("\n⚡ Ejecutando Triaje Algorítmico Fase 1 (Smart Relevance Scoring)...")
        from core.storage import run_smart_prescreening
        prescreen_results = run_smart_prescreening()
        print(f"✅ Triaje completado: {prescreen_results.get('screened_total', 0)} registros analizados.")
        print(f"   - Descartados por ruido temático o temporal en Fase 1: {prescreen_results.get('auto_excluded', 0)}")
        print(f"   - Candidatos con pertinencia que avanzan a revisión: {prescreen_results.get('prioritized', 0)}")

    # Números de flujo PRISMA finales
    flow = get_prisma_flow_numbers()
    export_project_snapshot()

    print("\n" + "=" * 70)
    print("📊 BALANCE CUANTITATIVO DEL FLUJO PRISMA TRAS LA COSECHA:")
    print("=" * 70)
    print(f"Total Registros Identificados:  {flow['total_identified']}")
    print(f"Duplicados Removidos:           {flow['duplicates_removed']}")
    print(f"Registros Únicos para Cribado:  {flow['records_screened']}")
    print(f"Excluidos en Fase 1:            {flow['records_excluded_phase1']}")
    print(f"Avanzan a Fase 2 (Texto C.):    {flow['full_text_assessed']}")
    print("=" * 70)

    return {
        "total_harvested_raw": total_harvested_raw,
        "inserted_count": inserted_count,
        "dedup_results": dedup_results,
        "prescreen_results": prescreen_results,
        "flow": flow
    }


def main():
    parser = argparse.ArgumentParser(description="PRISMA-ScR Autonomous Multi-API Harvester")
    parser.add_argument("--phases", type=str, default="1,2", help="Fases a cosechar separadas por coma: 1, 2, o all (default: 1,2)")
    parser.add_argument("--apis", type=str, default="openalex,europe_pmc,pubmed,crossref", help="APIs a consultar separadas por coma")
    parser.add_argument("--max", type=int, default=20, help="Máximo de registros por consulta por API (default: 20)")
    parser.add_argument("--no-dedup", action="store_true", help="No ejecutar deduplicación automática")
    parser.add_argument("--no-prescreen", action="store_true", help="No ejecutar pre-cribado algorítmico inteligente")

    args = parser.parse_args()

    phase_list = [p.strip() for p in args.phases.split(",") if p.strip()]
    api_list = [a.strip() for a in args.apis.split(",") if a.strip()]

    execute_harvest(
        phases=phase_list,
        apis=api_list,
        max_per_query_api=args.max,
        auto_dedup=not args.no_dedup,
        auto_prescreen=not args.no_prescreen
    )


if __name__ == "__main__":
    main()
