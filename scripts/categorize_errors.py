"""Aplica la categorización manual de los errores del clasificador.

Las categorías no se deducen con una regla automática: se asignaron leyendo los 25 mensajes mal
clasificados, uno por uno. Este script solo las vuelca sobre `reports/error_analysis.csv` a partir
del prefijo de cada texto, de modo que el resultado sea reproducible y quede claro cuál fue el
criterio en cada caso.

Uso:
    uv run python scripts/categorize_errors.py
"""

from __future__ import annotations

import pandas as pd

from inf8239_u02.config import ROOT

ENTRADA = ROOT / "reports/error_analysis.csv"
RESUMEN = ROOT / "reports/error_categories.csv"

#: Definición de cada categoría, para que el informe no dependa de interpretar su nombre.
DEFINICIONES = {
    "texto insuficiente":
        "Mensaje demasiado corto: pocas palabras y ninguna distintiva de su clase.",
    "léxico compartido":
        "Mensaje legítimo que usa palabras frecuentes en spam, como free, call u offer.",
    "aviso reenviado":
        "Advertencia legítima difundida en masa, con la forma de una campaña comercial.",
    "abreviaturas no estándar":
        "Mensaje legítimo escrito con las abreviaturas típicas del spam comercial.",
    "etiqueta discutible":
        "La etiqueta original es defendible en ambos sentidos; el error no es solo del modelo.",
    "spam conversacional":
        "Spam redactado como mensaje personal, sin números cortos, precios ni mayúsculas.",
    "notificación transaccional":
        "Spam con forma de confirmación de compra o de cargo.",
}

#: Categoría asignada a cada error, identificado por el comienzo de su texto.
CATEGORIAS: list[tuple[str, str]] = [
    # Falsos positivos: mensajes legítimos clasificados como spam
    ("Are you free now?can i call", "léxico compartido"),
    ("I'm at home. Please call", "texto insuficiente"),
    ("Glad to see your reply", "texto insuficiente"),
    ("I am waiting for your call sir", "léxico compartido"),
    ("I'm at work. Please call", "texto insuficiente"),
    ("Plz note: if anyone calling", "aviso reenviado"),
    ("Yes.. now only saw your message", "texto insuficiente"),
    ("Your daily text from me", "léxico compartido"),
    ("Sir, i am waiting for your call", "léxico compartido"),
    ("Hi Harish's rent has been", "abreviaturas no estándar"),
    ("Have you laid your airtel line", "léxico compartido"),
    ("I (Career Tel) have added u", "etiqueta discutible"),
    ("Total video converter free download", "léxico compartido"),
    ("Dont you have message offer", "texto insuficiente"),
    ("Please protect yourself from e-threats", "aviso reenviado"),
    # Falsos negativos: spam que pasó el filtro
    ("Latest News! Police station toilet", "etiqueta discutible"),
    ("dating:i have had two of these", "spam conversacional"),
    ("Sorry! U can not unsubscribe yet", "spam conversacional"),
    ("LookAtMe!: Thanks for your purchase", "notificación transaccional"),
    ("Hi this is Amy, we will be sending", "spam conversacional"),
    ("Babe: U want me dont u baby", "spam conversacional"),
    ("For sale - arsenal dartboard", "etiqueta discutible"),
    ("Sorry I missed your call let's talk", "spam conversacional"),
    ("CLAIRE here am havin borin time", "spam conversacional"),
    ("ASKED 3MOBILE IF 0870 CHATLINES", "etiqueta discutible"),
]


def categorizar(texto: str) -> str:
    for prefijo, categoria in CATEGORIAS:
        if str(texto).startswith(prefijo):
            return categoria
    return "sin clasificar"


def main() -> None:
    errores = pd.read_csv(ENTRADA)
    errores["category"] = errores["text"].map(categorizar)
    errores["definition"] = errores["category"].map(DEFINICIONES).fillna("")
    errores["error_type"] = errores.apply(
        lambda f: "falso positivo" if f["real"] == "ham" else "falso negativo", axis=1)

    pendientes = int((errores["category"] == "sin clasificar").sum())
    if pendientes:
        raise SystemExit(f"Quedan {pendientes} errores sin categorizar")

    errores.to_csv(ENTRADA, index=False, encoding="utf-8")

    resumen = (errores.groupby(["error_type", "category"]).size()
               .rename("errores").reset_index()
               .sort_values(["error_type", "errores"], ascending=[True, False]))
    resumen["definicion"] = resumen["category"].map(DEFINICIONES)
    resumen.to_csv(RESUMEN, index=False, encoding="utf-8")

    print(f"Errores categorizados: {len(errores)}")
    print(resumen.to_string(index=False))


if __name__ == "__main__":
    main()
