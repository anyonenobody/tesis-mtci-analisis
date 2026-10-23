# 📚 Lecciones Aprendidas y Registro de Errores Operativos

Este documento almacena de forma persistente los diagnósticos de fallos, causas raíz y reglas preventivas adoptadas en el proyecto para garantizar resiliencia analítica y cero regresiones.

---

### [2026-10-21] - Inyección de Fallback Multi-Proyecto en Herramientas Clonadas
* **Síntoma / Error:** `ModuleNotFoundError: No module named 'core'` al intentar invocar scripts clonados de `prisma-scr` desde `tesis-mtci-analisis`.
* **Causa Raíz:** Los scripts de `prisma-scr/tools` asumían que `REPO_ROOT` contenía el paquete `core` (e.g. `core.storage`, `core.api_fetcher`), el cual reside exclusivamente en el árbol del proyecto `prisma-scr`.
* **Solución Aplicada:** Se inyectó dinámicamente un bloque de resolución con fallback que detecta si el paquete `core` está localmente disponible en el espacio de trabajo; si no lo está, añade la ruta persistente de `prisma-scr` a `sys.path`.
* **Regla Preventiva:** Toda herramienta migrada o compartida entre proyectos debe incorporar detección condicional de contexto y no acoplarse rígidamente a rutas locales sin una ruta de respaldo documentada.

---

### [2026-10-21] - Dependencia Faltante `rapidfuzz` para Cotejo de Citas y Deduplicación
* **Síntoma / Error:** `ModuleNotFoundError: No module named 'rapidfuzz'` al inicializar `tools/db_cli.py` y `tools/verify_evidence_links.py`.
* **Causa Raíz:** El entorno virtual de `tesis-mtci-analisis` contaba con `pandas` y `python-docx`, pero carecía de la biblioteca de similitud difusa `rapidfuzz` requerida por los motores de auditoría documental.
* **Solución Aplicada:** Se ejecutó `uv add rapidfuzz`, actualizando coherentemente `pyproject.toml` y `uv.lock`.
* **Regla Preventiva:** Tras clonar herramientas especializadas, validar siempre las importaciones ejecutando `--help` o un pase de compilación (`python -m py_compile`) con el entorno virtual activo.

---

### [2026-10-22] - Diferenciación entre Índice (TOC) y Secciones Reales en document.xml
* **Síntoma / Error:** `References section spans characters 206011 to 206011 (Length: 0)` al delimitar la sección de bibliografía por regex sobre `document.xml`.
* **Causa Raíz:** La búsqueda de texto plano encuentra primero las entradas del Índice General (TOC), donde los títulos `15. Referencias` y `16. Anexos` están contiguos sin párrafos intermedios.
* **Solución Aplicada:** Emplear `python-docx` para localizar los objetos de párrafo con estilo `Heading 1` y calcular los índices en el elemento padre `parent.index(p._p)`, eliminando e insertando elementos con precisión de nivel DOM.
* **Regla Preventiva:** Nunca asumir que la primera aparición de un título en el XML corresponde a la sección del manuscrito; considerar siempre la presencia de tablas de contenido generadas previamente.

---

### [2026-10-22] - Construcción Segura de SDT en OOXML con lxml
* **Síntoma / Error:** `lxml.etree.XMLSyntaxError: xmlParseEntityRef: no name` al inyectar fragmentos XML de citas dinámicas.
* **Causa Raíz:** El texto de la cita o de los párrafos circundantes contenía caracteres ampersand (`&`) sin escapar al utilizar f-strings de Python.
* **Solución Aplicada:** Construir la jerarquía de elementos SDT mediante la API DOM de `etree.Element` y `etree.SubElement`, asignando el texto mediante la propiedad `.text` para delegar el escapado canónico a `lxml`.
* **Regla Preventiva:** Para manipulación de OpenXML en producción, evitar la interpolación directa de cadenas de texto de usuario dentro de fragmentos XML; utilizar siempre constructores de árbol DOM.

---

### [2026-10-22] - Sincronización Estricta de Tags en Citas Nativas y Administrador de Fuentes de Word
* **Síntoma / Error:** En Microsoft Word, ciertas citas (e.g. `Chafloque-Capuñay et al., 2025`) permitían "Editar cita" pero ocultaban "Editar fuente" en el menú contextual de clic derecho. Además, en el "Administrador de fuentes", múltiples referencias aparecían sin la marca de verificación (`✓` = fuente citada).
* **Causa Raíz:** Microsoft Word valida dinámicamente la correspondencia exacta (case-sensitive) entre el argumento del código de campo `{ CITATION Tag \l 3082 }` y el elemento `<b:Tag>` dentro de `customXml/item1.xml`. Si existe la menor discrepancia (e.g. guiones tipográficos como `Hernández-Sampieri2023` vs `HernándezSampieri2023`, o variantes de apellido como `Chafloque2025` vs `ChafloqueCapuñay2025`), Word considera la fuente no vinculada, suprimiendo "Editar fuente" y omitiendo el checkmark `✓`. Asimismo, fuentes sin campos en el cuerpo (como las matrices de evidencia en tablas clínicas o fuentes institucionales como OMS/SETEC/MINSA dejadas en texto estático) quedan sin marcar.
* **Solución Aplicada:** Se estandarizó un catálogo canónico de 56 tags alfanuméricos ASCII únicos. Se sincronizó `data/bibliografia_mtci.db`, `customXml/item1.xml` y los 101 campos dinámicos inyectados en párrafos del cuerpo y celdas de las tablas 1 y 8.
* **Regla Preventiva:** Antes de entregar documentos Word con bibliografía nativa, auditar con scripts de Word COM que `$doc.Bibliography.Sources.Count` coincida exactamente con el recuento de tags extraídos de los campos `CITATION` del manuscrito y que `$s.Cited` retorne `True` para el 100% de las fuentes.

---

### [2026-10-22] - Mapeo de Campos de Metadatos Ricos en el Motor de Bibliografía de Word (<b:DOI> vs <b:StandardNumber>)
* **Síntoma / Error:** Al hacer clic derecho sobre una cita en Word y seleccionar "Editar fuente", el formulario gráfico emergente mostraba campos vacíos marcados con asterisco rojo (`* Campo recomendado`), notablemente `* DOI`, `URL`, año o lugar de publicación (e.g. en leyes nicaragüenses como `Ley774_2012` o libros clásicos).
* **Causa Raíz:** El formulario nativo de Microsoft Word vincula el cuadro de texto rotulado `* DOI` exclusivamente al elemento XML `<b:DOI>`. Almacenar el DOI únicamente en `<b:StandardNumber>` deja vacía la casilla en la interfaz gráfica de Word. Asimismo, leyes, libros e informes institucionales carecían de elementos explícitos `<b:URL>`, `<b:City>`, `<b:CountryRegion>`, `<b:Publisher>`, `<b:Month>`, `<b:Day>` o `<b:PublicationTitle>` en `customXml/item1.xml`.
* **Solución Aplicada:**
  1. Enriquecimiento del esquema XML inyectando tanto `<b:DOI>` (DOI limpio sin prefijo URL) como `<b:StandardNumber>` para artículos con DOI.
  2. Búsqueda y verificación de URLs institucionales oficiales y legítimas para el 100% de las fuentes (e.g. repositorio oficial de la Asamblea Nacional de Nicaragua `legislacion.asamblea.gob.ni` para leyes y decretos, repositorios institucionales de UNAN-Managua, MINSA, OMS/OPS, y páginas de casas editoriales para libros de texto), sin inventar enlaces ni generar alucinaciones.
  3. Desglose completo de fecha (`<b:Year>`, `<b:Month>`, `<b:Day>`), ciudad, país y nombre de publicación (`<b:PublicationTitle>`).
* **Regla Preventiva:** Todo generador de `customXml/item1.xml` debe mapear simultáneamente `<b:DOI>` y `<b:StandardNumber>`, verificar la disponibilidad de enlaces oficiales en repositorios verificados, y auditar vía Word COM que `$source.Field("DOI")` y `$source.Field("URL")` contengan los valores requeridos sin disparar excepciones `HRESULT E_FAIL`.



