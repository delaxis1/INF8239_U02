"""Pruebas de la lectura del corpus comprimido.

El corpus se publica en ZIP y el miembro interior no trae encabezado, así que la conversión a CSV
es el punto donde un cambio en la fuente pasaría inadvertido. Estas pruebas no usan la red: arman
un ZIP en memoria con el mismo formato que el de UCI.
"""

from __future__ import annotations

import io
import zipfile

import pytest

from scripts.download_data import huella, leer_miembro

MIEMBRO = "SMSSpamCollection"
CONTENIDO = "ham\tOk lar... Joking wif u oni...\nspam\tWINNER!! Claim your prize now\n"


def zip_de_prueba(nombre: str = MIEMBRO) -> bytes:
    bufer = io.BytesIO()
    with zipfile.ZipFile(bufer, "w") as archivo:
        archivo.writestr(nombre, CONTENIDO)
    return bufer.getvalue()


def test_lee_el_miembro_sin_encabezado_y_nombra_las_columnas():
    marco = leer_miembro(zip_de_prueba(), MIEMBRO)
    assert list(marco.columns) == ["label", "text"]
    assert len(marco) == 2, "ninguna fila debe consumirse como encabezado"
    assert marco.loc[0, "label"] == "ham"
    assert marco.loc[1, "text"].startswith("WINNER")


def test_el_tabulador_no_parte_el_texto():
    """Si el separador llegara mal desde .env, el mensaje se cortaría en varias columnas."""
    marco = leer_miembro(zip_de_prueba(), MIEMBRO)
    assert marco.loc[0, "text"] == "Ok lar... Joking wif u oni..."


def test_falla_si_el_miembro_no_existe():
    with pytest.raises(KeyError, match="no está en el ZIP"):
        leer_miembro(zip_de_prueba(), "otro_archivo.txt")


def test_la_huella_cambia_si_cambia_un_byte():
    original = zip_de_prueba()
    assert len(huella(original)) == 64
    assert huella(original) != huella(zip_de_prueba("SMSSpamCollection_v2"))
