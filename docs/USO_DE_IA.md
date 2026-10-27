# Declaración de uso de asistentes de IA

**INF-8239 Ciencia de Datos II · Unidad 02 · Ejercicio 03** · Alexis De La Cruz · 100805370

El mandato exige declarar las herramientas utilizadas, los prompts relevantes, las partes
verificadas y las correcciones realizadas. Esto es lo que ocurrió.

## Herramienta

**Claude Opus 5 (Anthropic)**, utilizada a través de Claude Code, con acceso al proyecto local y al
aula virtual para leer el mandato y el manual de laboratorios.

## Instrucciones relevantes

Las instrucciones se recogen **resumidas en su contenido, no transcritas literalmente**.

| Instrucción dada al asistente | Qué determinó |
|---|---|
| Inicio del primer ejercicio de la Unidad 02 | Localizar el mandato, la rúbrica y los capítulos LAB04 y LAB05, y plantear el plan de trabajo |
| Entrega de los laboratorios guiados descargados, para confirmar que eran los correctos | Instalar el proyecto base del profesor y revisar su estructura antes de modificar nada |
| Instrucción de elegir el corpus | Comparar dos candidatos de UCI y justificar la selección y el descarte |

## Qué hizo el asistente

- Extendió `scripts/download_data.py` para admitir fuentes comprimidas, ya que el script base solo
  aceptaba un CSV directo y UCI publica este corpus en ZIP.
- Escribió `scripts/compare_models.py` y `scripts/categorize_errors.py`.
- Redactó los borradores de `docs/DATASET_CARD.md`, `docs/dataset_candidates.csv`, este archivo, el
  README y la conclusión.

## Qué verifiqué

- **Las huellas SHA-256** salen de ejecutar el script de descarga, no de un texto generado. El ZIP
  da `1587ea43…` y el CSV resultante `e227e264…`.
- **Las métricas** provienen de ejecutar `scripts/train_text.py` y `scripts/compare_models.py` en
  este equipo. Ningún número del informe se escribió a mano.
- **Los 25 errores se leyeron uno por uno** antes de asignarles categoría. Las categorías son un
  juicio propio sobre mensajes reales, no una clasificación automática; `categorize_errors.py` solo
  las vuelca al CSV para que el resultado sea reproducible.
- **Las pruebas** se ejecutan con `uv run pytest -q` y pasan.

## Correcciones durante el trabajo

- El `.env` guarda el separador como `\t` escapado. Al leerlo con `os.getenv` llegaba como dos
  caracteres y pandas lo habría tratado de forma ambigua, así que se decodifica explícitamente antes
  de usarlo.
- Se añadió una comprobación del número de filas esperadas (5 574). Si la fuente cambiara, el script
  falla en lugar de continuar con datos distintos en silencio.
- La selección automática del script base es la regresión logística, por F1 macro. Al revisar el
  costo de cada tipo de error concluí que esa elección merece discusión, y así quedó escrito en la
  conclusión en lugar de aceptarla sin más.

## Responsabilidad

Los datos, el código, las referencias y las conclusiones son responsabilidad mía. Puedo explicar
cualquier fragmento del proyecto, y las decisiones metodológicas —eliminar duplicados antes de
particionar, usar F1 macro en lugar de exactitud, discutir el umbral a partir del costo del error—
están justificadas en la conclusión y en la ficha del dataset.
