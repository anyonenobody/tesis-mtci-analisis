# 🌿 Directrices de Proyecto para Claude Code: Tesis MTCI (UNAN-Managua)

Este archivo (`CLAUDE.md`) es la guía operacional y metodológica primaria para **Claude Code**. Define la arquitectura, reglas de diseño, contexto epistemológico y el pipeline técnico para generar la presentación oficial de defensa de tesis.

---

## 🎯 1. Misión Principal y Estado Actual

* **Objetivo:** Generar la presentación ejecutiva final de defensa de licenciatura en formato PowerPoint nativo widescreen 16:9: `Presentacion_Defensa_Tesis_MTCI_UNAN.pptx`.
* **Diagnóstico Previo (Por qué NO Python):**
  - Los scripts basados en `python-pptx` generaron diapositivas rígidas, cajas genéricas ("no-cards failure"), viñetas monótonas y tipografía desbalanceada sin impacto visual.
  - La versión interactiva en HTML espacial funciona como prototipo, pero **el tribunal examinador exige un archivo .pptx nativo, autónomo y editable** para la sala de conferencias.
* **Solución Mandatoria:**
  - Desarrollar la presentación mediante **Node.js y `pptxgenjs`** apoyándose en la suite instalada en `presentacion_defensa/` y en el skill corporativo `.agents/skills/pptx/SKILL.md`.
  - Iconos vectoriales nítidos generados con `react-icons` + `sharp` vía `presentacion_defensa/icon_helper.js`.
  - Inserción de gráficas empíricas oficiales de alta resolución desde `assets/figuras_apa7/`.

---

## 🏛️ 2. Metadatos de la Investigación y Datos Empíricos (Cero Alucinación)

* **Título:** *La Medicina Tradicional, Complementaria e Integrativa (MTCI) como Complemento en la Atención Psicológica: Estudio Mixto con Estudiantes, Facilitadores Locales y Docentes de Psicología del CUR-Estelí*
* **Institución:** Universidad Nacional Autónoma de Nicaragua, Managua (UNAN-Managua), Centro Universitario Regional Estelí (CUR-Estelí). Carrera de Psicología, 2026.
* **Autores:** Dina Fabiola García Torres, Tatiana Paola López Ramos, Engel Enoc Zamora Velásquez.
* **Docente Tutora:** Dr. Tania Libertad Pérez Guevara.
* **Población y Muestra Total ($N = 86$ actores):**
  - **68 estudiantes** de Psicología (1.º a 5.º año académico).
  - **10 facilitadores locales / terapeutas tradicionales** de Estelí.
  - **8 docentes** de la carrera de Psicología del CUR-Estelí.
* **Tensión Jurídica Central:**
  - **Ley N.º 774** (Medicina Natural, Terapias Complementarias y Productos Naturales): Reconoce y promueve el derecho ciudadano y la integración en salud.
  - **Ley N.º 292** (Medicamentos y Farmacias): Establece la frontera legal de **no prescripción** médica por parte del psicólogo (delimitación estricta del ejercicio profesional).
* **Paradoja Empírica:**
  - $94.1\%$ de estudiantes considera pertinente la MTCI para la psicología y el $98.5\%$ desea formación curricular.
  - Sin embargo, el **$89.7\%$ desconoce la Ley 774** y existe un vacío curricular del $100\%$ en materias formales.
  - El **$100\%$ de docentes** respalda la integración curricular bajo enfoque de salud mental intercultural y ético.
* **Propuesta Aplicada:** Anexo 16.2 — *Manual de Estrategias para la Integración de la MTCI en la Práctica Psicológica: Protocolo de Derivación y Acompañamiento Interdisciplinario* (`docs/capitulos/05_propuesta_manual.md` y `assets/extracted/portada_manual.jpg`).

---

## 🎨 3. Estándar de Diseño Editorial y Reglas Estrictas de PPTXGenJS

Sigue rigurosamente las lecciones de `.agents/skills/pptx/SKILL.md`:

### Reglas Críticas de `pptxgenjs` (Evitar Corrupción de Archivos):
1. **Códigos Hexadecimales:** SIEMPRE 6 caracteres alfanuméricos **SIN `#`** (ejemplo: `color: "1B365D"`, NUNCA `color: "#1B365D"` ni 8 dígitos).
2. **Dimensiones:** Usar `pres.layout = "LAYOUT_WIDE"` (13.333" × 7.5"). Configurar antes de crear diapositivas.
3. **Inmutabilidad de Opciones:** `pptxgenjs` muta los objetos de opciones internamente (los convierte a EMU en el primer uso). **Nunca compartas un mismo objeto de opciones o de sombra** entre llamadas; genera un objeto nuevo cada vez.
4. **Sombras:** `offset` debe ser mayor o igual a 0 (un valor negativo corrompe el XML).
5. **Alineación de Texto:** Aplica `margin: 0` en cuadros de texto cuando requieras alineación exacta con líneas o iconos.
6. **Notas de Oratoria Obligatorias:** Cada diapositiva DEBE contener su guion en `slide.addNotes("...")` con instrucciones de tiempo (1-2 min), modulación de voz y puntos clave a defender ante el tribunal.
7. **Diseño Visual-First (No-Cards & No-Bullets Laundry):**
   - Cero bloques interminables de texto o listas de viñetas genéricas.
   - Cada lámina debe tener un **foco visual protagónico**: una gráfica empírica (`assets/figuras_apa7/`), una estadística destacada (KPI gigante: `89.7%`, `100%`), o un flujo de proceso con iconos de `react-icons`.

### Paleta Institucional UNAN / MTCI (`presentacion_defensa/theme.js`):
- **Azul Institucional UNAN:** `"1B365D"` (Primario, títulos, autoridad académica).
- **Verde Salvia Botánico:** `"6B8F7A"` (Acento MTCI, plantas, naturaleza, equilibrio).
- **Azul Clínico:** `"2E86AB"` (Psicología, datos empíricos, métricas secundarias).
- **Naranja / Ámbar Cálido:** `"E6955F"` (Alertas normativas, contrastes, paradojas).
- **Fondo Lienzo:** `"F8F9FA"` (Blanco roto limpio) o `"FFFFFF"`.
- **Texto Principal:** `"1F2937"` (Slate oscuro de alta legibilidad).

---

## 📑 4. Estructura Canónica de la Defensa (18 Diapositivas / 20 Minutos)

| N.º | Título / Tema | Enfoque Visual Dominante | Gráfica / Recurso |
| :---: | :--- | :--- | :--- |
| **01** | **Portada Institucional** | Escudo UNAN, título sobrio, autores, tutora y año 2026 | `assets/extracted/unan_logo_clean.png` |
| **02** | **Problema y Tensión Jurídica** | Dicotomía Ley 774 (derecho) vs. Ley 292 (límite no-prescripción) | Iconos `FaBalanceScale` + `FaUserShield` |
| **03** | **Antecedentes de la Investigación** | Línea de tiempo: OMS (2014-2025) → Región → Nicaragua | Flujo horizontal de 3 hitos temporales |
| **04** | **Contexto Territorial e Institucional** | Estelí etnobotánico vs. formación hegemónica en CUR-Estelí | `presentacion_defensa/assets/mapa_cur.png` |
| **05** | **Objetivos de la Investigación** | Objetivo General y 3 Específicos articulados a los 3 estamentos | 3 pilares estructurados con iconos |
| **06** | **Diseño Metodológico** | Enfoque mixto concurrente, muestra $N = 86$ y técnicas aplicadas | Triangulación metodológica (Diagrama) |
| **07** | **Estudiantes: Percepción y Brecha** | Paradoja: 94.1% interés vs. 89.7% desconocimiento legal | `assets/figuras_apa7/figura_04_dominio_conceptual_normativo_estudiantes.png` |
| **08** | **Estudiantes: Prácticas y Frecuencia** | Fitoterapia, masajes, yoga, relajación y autocuidado | `assets/figuras_apa7/figura_07_frecuencia_uso_estudiantes.png` |
| **09** | **Facilitadores: Saberes y Territorio** | Perfil sociodemográfico, experiencia y prácticas vivas | `assets/figuras_apa7/figura_12_practicas_actores_locales.png` |
| **10** | **Facilitadores: Salud Mental** | Ansiedad, estrés, depresión y somatizaciones en la comunidad | `assets/figuras_apa7/figura_14_apertura_emocional_usuarios_actores.png` |
| **11** | **Facilitadores: Barreras y Estigma** | Desarticulación con el modelo biomédico y reservas culturales | `assets/figuras_apa7/figura_17_dificultades_normativas_actores.png` |
| **12** | **Docentes: Postura Epistémica** | Caracterización docente y valoración de la salud intercultural | `assets/figuras_apa7/figura_22_especialidad_docentes.png` |
| **13** | **Docentes: Respaldo Curricular** | 100% apoyo a la integración curricular en la carrera | `assets/figuras_apa7/figura_24_estrategias_academicas_docentes.png` |
| **14** | **Triangulación Multiactor** | Matriz comparativa: Estudiantes vs. Facilitadores vs. Docentes | Matriz de 3 columnas con convergencias |
| **15** | **Conclusiones Epistémicas** | 4 conclusiones directas y rigurosas sin generalizaciones | 4 bloques de impacto con métricas |
| **16** | **Recomendaciones Estratégicas** | Recomendaciones para UNAN-Managua, MINSA y práctica clínica | 3 ejes con iconos de acción |
| **17** | **Propuesta Aplicada: Manual MTCI** | Protocolo de derivación, competencias y ética profesional | `presentacion_defensa/assets/portada_manual_banda.jpg` |
| **18** | **Cierre y Agradecimientos** | Agradecimiento al Tribunal Examinador y cita de cierre solemne | Escudo UNAN institucional |

---

## 🛠️ 5. Flujo de Trabajo y Comandos de Ejecución

1. **Dependencias:**
   - Ya están instaladas en `presentacion_defensa/node_modules/` (`pptxgenjs`, `react`, `react-dom`, `react-icons`, `sharp`).
2. **Generar la Presentación:**
   ```bash
   node presentacion_defensa/generate_deck.js
   ```
   *(El script debe guardar el archivo en la raíz: `Presentacion_Defensa_Tesis_MTCI_UNAN.pptx`)*.
3. **Validar la Estructura OOXML:**
   ```bash
   python .agents/skills/pptx/scripts/office/validate.py Presentacion_Defensa_Tesis_MTCI_UNAN.pptx
   ```
   *(Garantiza que no existan errores de esquema o corrupción antes de abrir en Microsoft PowerPoint)*.
4. **Generar Vistas Previas (Thumbnails):**
   ```bash
   python .agents/skills/pptx/scripts/thumbnail.py Presentacion_Defensa_Tesis_MTCI_UNAN.pptx thumbs-defensa
   ```

---

## 📂 6. Localización de Archivos Clave del Repositorio

- **Capítulos de la Tesis:** `docs/capitulos/` (Especialmente `01_introduccion.md`, `03_diseno_metodologico.md`, `04_analisis_y_discusion_resultados.md`, `05_propuesta_manual.md`, `06_conclusiones_y_recomendaciones.md`).
- **Catálogo de Figuras APA 7:** `docs/catalogo_figuras_apa7.md`.
- **Imágenes Gráficas:** `assets/figuras_apa7/` (Figuras 1 a 25 en PNG alta resolución).
- **Recursos Auxiliares:** `presentacion_defensa/assets/` (mapa, fondos, nubes de palabras, manual).
- **Skill de Presentaciones Anthropic:** `.agents/skills/pptx/SKILL.md`.
- **Ayudante de Iconos:** `presentacion_defensa/icon_helper.js`.
- **Tokens y Tema:** `presentacion_defensa/theme.js`.
