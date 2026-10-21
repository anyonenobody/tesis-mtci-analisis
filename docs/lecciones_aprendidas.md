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

### [2026-10-21] - Omitir Paréntesis o Escapado en Comandos PowerShell de Una Línea
* **Síntoma / Error:** `SyntaxError: '(' was never closed` y `SyntaxError: invalid syntax` al pasar cadenas con comillas escapadas complejas a `python -c` dentro de PowerShell.
* **Causa Raíz:** El parser de PowerShell interpreta comillas dobles, caracteres de escape (`\`) y saltos de línea de manera distinta a Bash en scripts en línea.
* **Solución Aplicada:** Emplear scripts de PowerShell nativos (`System.IO.File` o `-replace`) o archivos de script dedicados en lugar de bloques complejos de `python -c` embebidos con comillas anidadas.
* **Regla Preventiva:** Para modificaciones de texto en lote sobre Windows, privilegiar cmdlets nativos de PowerShell con codificación UTF-8 explícita.
