# INF8239_U02 · Clasificador de texto reproducible

**INF-8239 Ciencia de Datos II · Unidad 02 · Ejercicio 03** · Alexis De La Cruz · Matrícula 100805370
Maestría en Ciencias de Datos e Inteligencia Artificial (UASD)

Construido sobre el proyecto base del curso (autor académico: Edwin Ramón José Nolasco), siguiendo
los laboratorios LAB04 y LAB05.

> ¿Puede un clasificador entrenado solo con el texto de un SMS separar el spam de los mensajes
> legítimos, y a qué costo en mensajes legítimos bloqueados?

## Resultados

Conjunto de prueba: 1 290 mensajes (25 %), de los cuales 160 son spam.

| Modelo | F1 macro | Precisión spam | Recall spam | Legítimos bloqueados | Spam que pasa |
|---|---|---|---|---|---|
| Regresión logística | **0.956** | 0.909 | **0.938** | 15 | 10 |
| Complement Naive Bayes | 0.933 | **0.963** | 0.812 | **5** | 30 |
| Dummy (clase mayoritaria) | 0.467 | 0.000 | 0.000 | 0 | 160 |

La logística gana en F1 macro, pero bloquea tres veces más mensajes legítimos. Pasar de Naive Bayes
a la logística cuesta **un mensaje real perdido por cada dos spam atrapados**. La discusión completa
está en [`reports/conclusion.md`](reports/conclusion.md).

## Dataset

| | |
|---|---|
| Corpus | SMS Spam Collection v.1 · [UCI id 228](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) |
| Licencia y DOI | CC BY 4.0 · [10.24432/C5CC84](https://doi.org/10.24432/C5CC84) |
| Tamaño | 5 574 mensajes · 86.6 % `ham`, 13.4 % `spam` |
| Duplicados | 414 textos repetidos, eliminados antes de particionar |
| Ficha completa | [`docs/DATASET_CARD.md`](docs/DATASET_CARD.md) · candidatos en [`docs/dataset_candidates.csv`](docs/dataset_candidates.csv) |

Los datos no se versionan: se obtienen ejecutando el script, que verifica la huella SHA-256 y el
número de filas esperado.

## Instalación y ejecución

Requiere [uv](https://docs.astral.sh/uv/). No cree el entorno a mano.

```bash
uv python install 3.12
uv sync
uv run pytest -q
```

Copie `.env.example` como `.env`; ya viene configurado para este corpus. Después:

```bash
uv run python scripts/download_data.py     # descarga, verifica SHA-256 y escribe data/raw/dataset.csv
uv run python scripts/audit_data.py        # filas, nulos, duplicados, clases y longitudes
uv run python scripts/train_text.py        # baseline + Naive Bayes + regresión logística
uv run python scripts/compare_models.py    # métricas por clase y conteo de cada tipo de error
uv run python scripts/categorize_errors.py # vuelca la categorización manual de los 25 errores
uv run streamlit run app/streamlit_app.py  # aplicación local
```

Todo el proceso tarda menos de un minuto en un equipo de escritorio.

## Qué genera

| Archivo | Contenido |
|---|---|
| `reports/text_metrics.csv` | Métricas por modelo, incluidos los errores de cada tipo |
| `reports/confusion_text.png` | Matriz de confusión del modelo seleccionado |
| `reports/error_analysis.csv` | Los 25 errores con su categoría y su definición |
| `reports/error_categories.csv` | Resumen por tipo de error y categoría |
| `reports/conclusion.md` | Conclusión interpretada |
| `models/text_model.joblib` | Pipeline entrenado, listo para reutilizar |

## Análisis de errores

Los 25 errores del modelo seleccionado se leyeron uno por uno y se agruparon en siete categorías:

| Tipo | Categoría | Casos |
|---|---|---|
| Falso positivo | Léxico compartido con spam | 6 |
| Falso positivo | Texto insuficiente | 5 |
| Falso positivo | Aviso reenviado | 2 |
| Falso positivo | Abreviaturas no estándar | 1 |
| Falso positivo | Etiqueta discutible | 1 |
| Falso negativo | Spam conversacional | 6 |
| Falso negativo | Etiqueta discutible | 3 |
| Falso negativo | Notificación transaccional | 1 |

El patrón dominante: los mensajes legítimos se bloquean por ser cortos o por usar palabras de spam,
y el spam que pasa está escrito como una conversación personal.

## Pruebas

```bash
uv run pytest -q
```

| Archivo | Qué comprueba |
|---|---|
| `tests/test_data_contract.py` | Columnas requeridas, textos no vacíos, al menos dos clases y el contrato del corpus real |
| `tests/test_text_model.py` | Los tres pipelines predicen y conservan vectorizador y estimador |
| `tests/test_download.py` | La lectura del miembro del ZIP y el rechazo de un miembro inexistente |

## Estructura

```
INF8239_U02/
├── app/streamlit_app.py       aplicación local
├── data/raw/                  datos descargados (no versionados)
├── docs/
│   ├── DATASET_CARD.md        ficha, diccionario, población y riesgos
│   ├── dataset_candidates.csv los dos candidatos y la justificación
│   └── USO_DE_IA.md           declaración de uso de IA
├── reports/                   métricas, matriz, errores y conclusión
├── scripts/                   descarga, auditoría, entrenamiento, comparación y categorización
├── src/inf8239_u02/           configuración, datos y modelos
├── tests/
├── pyproject.toml
└── uv.lock
```

## Entorno

Windows 11 · Intel Core i9-13980HX con 16 GB de RAM · Python 3.12 gestionado por uv ·
scikit-learn 1.5 · El entorno se reproduce con `uv sync` a partir de `uv.lock`.

## Declaración de uso de asistentes de IA

Este proyecto se desarrolló con la asistencia de Claude Opus 5 (Anthropic). El detalle de qué hizo
la herramienta, qué prompts se usaron, qué verifiqué y qué correcciones hice está en
[`docs/USO_DE_IA.md`](docs/USO_DE_IA.md), como exige el mandato del ejercicio.

## Licencia y uso

Código académico para INF-8239. El corpus pertenece a sus autores y se usa bajo CC BY 4.0, citando:
Almeida, T. A., Gómez Hidalgo, J. M., y Yamakami, A. (2011). *Contributions to the study of SMS spam
filtering*. ACM DocEng.
