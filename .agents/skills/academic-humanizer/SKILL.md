---
name: academic-humanizer
description: >-
  Humanize academic texts, research papers, and thesis chapters to bypass
  AI detectors (such as Turnitin, GPTZero, CopyLeaks) while elevating
  scholarly rigor, burstiness, natural linguistic cadence, and authentic voice.
  Use whenever the user requests humanizing, making text undetectable to AI
  checkers, eliminating robotic phrasing, or refining academic drafts to sound
  genuinely human.
---

# Academic Humanizer & Authenticity Skill

This skill guides the rewriting and humanization of academic texts, thesis chapters, scientific papers, and research proposals to ensure they read with the natural cadence, variability, and intellectual depth of an experienced human scholar, bypassing AI classifiers like **Turnitin AI Detection**, **GPTZero**, and **CopyLeaks**.

---

## 🔬 How AI Detectors Work (And How to Defeat Them)

AI detectors do not "understand" text; they measure two statistical properties:

1. **Perplexity (Incertidumbre léxica)**:
   - LLMs generate words with maximum statistical probability given preceding tokens (low perplexity).
   - *Humanization rule*: Introduce context-specific vocabulary, idiomatic academic phrasing, domain-specific terminology, and organic Latin American scholarly syntax that generic LLMs never choose by default.

2. **Burstiness (Variabilidad rítmica y sintáctica)**:
   - LLMs write with nearly uniform sentence lengths (18–25 words), flat paragraph structures, and rhythmic predictability.
   - *Humanization rule*: Maximize burstiness. Intentionally interlace short, assertive punchy sentences (6–10 words) with complex, clause-rich analytical sentences (30–45 words). Standard deviation of sentence length must exceed **9.0 words**.

3. **Structural Symmetry & Predictable Transition Templates**:
   - LLMs rely on predictable connectors at sentence starts (*Asimismo... En este sentido... Por consiguiente... Frente a este escenario... Cabe destacar...*).
   - LLMs generate balanced bullet points that follow identical grammatical formulas (e.g. `[Título]: [Verbo en infinitivo/presente...]`).
   - *Humanization rule*: Break symmetry. Embed transitional thoughts within the clause (using em-dashes, semicolons, parenthetical comments) and vary paragraph entry points.

---

## 🚫 Lexical Blacklist (AI Clichés in Spanish Academic Writing)

Never use these robotic patterns:
| Formulaic AI Phrase | Natural Human Alternative |
| :--- | :--- |
| *De creciente relevancia / De vital importancia* | *Adquiere notoriedad / Cobra fuerza / Se vuelve objeto de debate* |
| *En este escenario / Frente a esta problemática* | *Bajo estas circunstancias / En la práctica local / En este marco* |
| *Andamiaje metodológico / Andamiaje teórico* | *Estructura analítica / Soporte metodológico / Enfoque* |
| *Un tapiz de saberes / Un compendio de* | *Diversidad de tradiciones / Confluencia de prácticas* |
| *Esclarecedor / Arroja luz* | *Ilustra / Sugiere / Permite constatar* |
| *Un vacío crítico / Una desconexión crítica* | *Una brecha formativa concreta / La falta de directrices formales* |
| *Cabe destacar / Es menester subrayar* | *Conviene advertir / Es preciso notar / Un dato elocuente es que* |
| *Asimismo / Por consiguiente (al inicio de cada párrafo)* | Conectores integrados orgánicamente (*Esto explica por qué...*, *De ahí que...*, *Sin embargo...*) |
| *Desempeña un papel fundamental / Juega un rol crucial* | *Condiciona directamente / Incide de manera palpable* |

---

## ✍️ 5 Golden Principles for Undetectable Academic Spanish

### 1. Organic Rhythm & Varied Sentence Length
Mix sentence tempos within every paragraph:
- **Corta:** *La ley existe, pero no se enseña.* (7 palabras)
- **Larga y compleja:** *Aunque la Ley No. 774 reconoce a la medicina natural como un derecho ciudadano dentro del sistema público de salud, en las aulas universitarias el debate sobre cómo articular estos saberes con la psicoterapia formal continúa ausente, dejando a los estudiantes en una suerte de limbo procedimental.* (44 palabras)

### 2. Situated Reality (Anclaje territorial y vivencial)
Replace abstract generalities with grounded facts from the local setting:
- *Genérico IA:* "Los actores locales expresaron percepciones positivas respecto a la integración holística."
- *Humano situado:* "En los barrios y comarcas de Estelí, el recurso a la botánica o al trabajo corporal suele anteceder por meses —o incluso años— a la primera consulta con un psicólogo."

### 3. Modulación Epistémica (Evitar absolutismos)
AI loves absolute statements (*"confirma categóricamente que..."*). Human academics use calibrated caution:
- *"Los datos no apuntan a una sustitución del tratamiento, sino a una búsqueda de alivio sintomático previo."*
- *"Lejos de constituir un rechazo a la ciencia convencional, lo que se observa es..."*

### 4. Puntuación Humana Expresiva
Use semicolons (`;`), em-dashes (`—...—`), and colons (`:`) naturally to break up monolithic comma-separated clauses.

### 5. Asimetría en Esquemas y Listados
When summarizing chapters or sections, weave them together as an analytical journey rather than a mechanical catalog of cloned bullet points.

---

## 🛠️ Verification Tool
Test any rewritten text using the bundled detector script:
```bash
uv run python .agents/skills/academic-humanizer/scripts/detect_ai_patterns.py --text "Tu texto aquí..."
# O pasando un archivo:
uv run python .agents/skills/academic-humanizer/scripts/detect_ai_patterns.py "ruta_archivo.md"
```
Ensure:
- Sentence length standard deviation $> 9.0$
- Zero AI clichés from the blacklist
- Type-Token Ratio (TTR) $> 0.50$
