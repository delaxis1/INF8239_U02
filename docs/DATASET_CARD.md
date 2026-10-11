# Dataset Card · SMS Spam Collection

**INF-8239 Ciencia de Datos II · Unidad 02 · Ejercicio 03** · Alexis De La Cruz · 100805370

## Identificación

- **Nombre:** SMS Spam Collection v.1
- **Fuente original:** UCI Machine Learning Repository, id 228 ·
  <https://archive.ics.uci.edu/dataset/228/sms+spam+collection> · DOI 10.24432/C5CC84
- **Responsable:** Tiago A. Almeida (Universidade Federal de São Carlos) y José María Gómez Hidalgo
- **Versión o fecha:** v.1, donada el 22 de junio de 2012
- **Licencia:** Creative Commons Attribution 4.0 International (CC BY 4.0), que permite descargar,
  analizar y publicar resultados derivados citando la fuente
- **Idioma:** inglés, con las abreviaturas y la ortografía propias del SMS

## Propósito y variable objetivo

La pregunta del ejercicio es: **¿puede un clasificador entrenado solo con el texto del mensaje
separar el spam de los mensajes legítimos lo bastante bien como para filtrarlos automáticamente, y
a qué costo en mensajes legítimos bloqueados?**

La variable objetivo es `label`, con dos valores: `ham` (mensaje legítimo) y `spam`. La unidad de
análisis es un mensaje SMS individual. El error caro no es el spam que pasa, sino el mensaje
legítimo bloqueado: un SMS de trabajo o de un familiar que nunca llega cuesta más que un anuncio
que sí llega.

## Diccionario de datos

| Columna | Tipo | Descripción | Valores o unidad |
|---|---|---|---|
| `label` | texto, categórica | Clase asignada por los autores del corpus | `ham` (4 827; 86.6 %) · `spam` (747; 13.4 %) |
| `text` | texto libre | Contenido completo del mensaje, tal como se recibió | 2 a 910 caracteres; mediana 62, p90 156, p99 276 |

Cinco ejemplos reales del corpus:

| `label` | `text` |
|---|---|
| ham | `I'm at home. Please call` |
| ham | `Glad to see your reply.` |
| ham | `Yes.. now only saw your message..` |
| spam | `Sorry! U can not unsubscribe yet. THE MOB offer package has a min term of 54 weeks` |
| spam | `LookAtMe!: Thanks for your purchase of a video clip, you've been charged 35p.` |

No se aplicó ninguna transformación al texto: el vectorizador TF-IDF trabaja sobre el contenido
original. La decisión se documenta porque cualquier limpieza previa cambiaría los resultados.

## Procedimiento de obtención

`uv run python scripts/download_data.py` descarga el ZIP público, informa su huella SHA-256, extrae
el miembro `SMSSpamCollection` —que no trae encabezado y viene separado por tabuladores—, comprueba
que tenga exactamente 5 574 filas y lo guarda como `data/raw/dataset.csv` con las columnas `label` y
`text`.

| Elemento | Valor |
|---|---|
| SHA-256 del ZIP descargado | `1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3` |
| SHA-256 del CSV generado | `e227e264baf1a64f5aa6e49cd5d371c26cbd77c8952de3fa2e6e2fda3c3403cf` |

Si la fuente cambiara, el conteo de filas falla de forma explícita en lugar de continuar en
silencio. Los datos no se versionan en Git: se obtienen ejecutando el script.

## Calidad observada

Medido con `uv run python scripts/audit_data.py`:

- **5 574 filas y 2 columnas.** Sin valores nulos en ninguna de las dos.
- **414 textos duplicados**, un 7.4 % del corpus. Se eliminan antes de particionar, porque un mismo
  mensaje en entrenamiento y en prueba infla artificialmente el desempeño.
- **Clases desbalanceadas:** 86.6 % frente a 13.4 %. La exactitud resulta engañosa y por eso la
  métrica principal es el F1 macro.
- **Longitudes:** mediana 62 caracteres, p99 276, máximo 910. El mínimo de 2 caracteres anticipa el
  problema que después apareció en el análisis de errores: hay mensajes demasiado cortos para
  clasificarse por su contenido.

## Población cubierta y excluida

El corpus combina cuatro fuentes: 425 mensajes de spam recogidos del foro británico Grumbletext,
3 375 mensajes legítimos del NUS SMS Corpus de Singapur —en su mayoría de estudiantes
universitarios—, 450 mensajes legítimos de una tesis doctoral y 1 324 del SMS Spam Corpus v.0.1 Big.

Queda fuera cualquier idioma distinto del inglés, el español incluido; el spam posterior a 2012, que
hoy usa otras plataformas y otros formatos; y poblaciones no universitarias o de otras regiones. Un
modelo entrenado aquí no debería aplicarse a mensajes en español ni a campañas actuales sin volver a
medir.

## Riesgos, sesgos y usos prohibidos

- **Sesgo de época y de plataforma.** El spam de 2012 se reconoce por números cortos, precios en
  libras y mayúsculas. El spam actual imita cada vez más una conversación normal, y el análisis de
  errores lo confirma: 6 de los 10 que pasaron el filtro están escritos como mensajes personales.
- **Etiquetas discutibles.** Al leer los 25 errores aparecieron 4 casos donde la etiqueta original
  es defendible en ambos sentidos. Parte del techo del modelo no es del modelo.
- **Contenido sensible.** Algunos mensajes incluyen lenguaje sexual explícito y números de teléfono
  de 2012. No deben publicarse ejemplos sin revisarlos antes.
- **Uso prohibido.** No debe usarse para identificar personas, ni como filtro en producción sin una
  validación con datos actuales y una política explícita sobre el mensaje legítimo bloqueado.
