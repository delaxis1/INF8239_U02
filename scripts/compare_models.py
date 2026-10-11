"""Compara los tres pipelines con métricas por clase y el conteo real de cada tipo de error.

`train_text.py` informa el F1 macro y guarda el modelo. Este script añade lo que hace falta para
decidir: cuántos mensajes legítimos bloquea cada modelo y cuánto spam deja pasar, que en este
problema no cuestan lo mismo.

Usa exactamente la misma partición que `train_text.py`: misma semilla, mismo `test_size` y el mismo
descarte de duplicados, de modo que las cifras sean comparables.

Uso:
    uv run python scripts/compare_models.py
"""

from __future__ import annotations

import pandas as pd
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from inf8239_u02.config import ROOT, settings
from inf8239_u02.data import load_dataset, validate_dataframe
from inf8239_u02.modeling import build_models

SALIDA = ROOT / "reports/text_metrics.csv"
POSITIVA = "spam"


def preparar():
    """Misma preparación que train_text.py: sin nulos, sin duplicados y partición estratificada."""
    df = load_dataset().dropna(subset=[settings.text_column, settings.target_column])
    antes = len(df)
    df = df.drop_duplicates(subset=[settings.text_column])
    validate_dataframe(df, settings.text_column, settings.target_column)
    print(f"Filas: {antes} -> {len(df)} tras eliminar {antes - len(df)} duplicados de texto")
    return train_test_split(
        df[settings.text_column], df[settings.target_column], test_size=0.25,
        random_state=settings.random_state, stratify=df[settings.target_column])


def main() -> None:
    x_train, x_test, y_train, y_test = preparar()
    print(f"Entrenamiento: {len(x_train)} · Prueba: {len(x_test)} "
          f"({(y_test == POSITIVA).sum()} spam)")

    filas = []
    for nombre, modelo in build_models(settings.random_state).items():
        modelo.fit(x_train, y_train)
        pred = modelo.predict(x_test)
        # La matriz se ordena [ham, spam]: fila real, columna predicha.
        (vn, fp), (fn, vp) = confusion_matrix(y_test, pred, labels=["ham", POSITIVA])
        filas.append({
            "model": nombre,
            "f1_macro": f1_score(y_test, pred, average="macro"),
            "precision_spam": precision_score(y_test, pred, pos_label=POSITIVA, zero_division=0),
            "recall_spam": recall_score(y_test, pred, pos_label=POSITIVA, zero_division=0),
            "recall_ham": recall_score(y_test, pred, pos_label="ham", zero_division=0),
            "legitimos_bloqueados": int(fp),
            "spam_que_pasa": int(fn),
            "spam_detectado": int(vp),
        })

    tabla = pd.DataFrame(filas).sort_values("f1_macro", ascending=False)
    tabla.to_csv(SALIDA, index=False, encoding="utf-8")
    pd.set_option("display.width", 160)
    print()
    print(tabla.round(3).to_string(index=False))
    print(f"\nGuardado en {SALIDA.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
