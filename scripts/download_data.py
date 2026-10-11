"""Descarga el corpus desde su fuente pública y lo deja normalizado en data/raw/dataset.csv.

Admite tres modos, controlados desde .env:

- `DATA_SOURCE=local`: el archivo ya está en disco; solo informa su ruta y su huella.
- `DATA_SOURCE=url` con un CSV: lo descarga tal cual.
- `DATA_SOURCE=url` con un ZIP: lo descarga, informa la huella del comprimido, extrae el miembro
  indicado en `DATASET_ZIP_MEMBER` y lo convierte a CSV con las columnas configuradas.

El tercer modo es el que necesita SMS Spam Collection: UCI lo publica comprimido y el archivo
interior no trae encabezado, viene separado por tabuladores y en orden etiqueta-texto.
"""

from __future__ import annotations

import hashlib
import io
import os
import sys
import zipfile

import pandas as pd
import requests

from inf8239_u02.config import ROOT, settings
from inf8239_u02.data import sha256

DESTINO = ROOT / "data/raw/dataset.csv"
TIEMPO_LIMITE = 60


def descargar(url: str) -> bytes:
    """Descarga el recurso y devuelve sus bytes, fallando de forma explícita."""
    respuesta = requests.get(url, timeout=TIEMPO_LIMITE)
    respuesta.raise_for_status()
    if not respuesta.content:
        raise ValueError(f"La fuente devolvió un archivo vacío: {url}")
    return respuesta.content


def huella(contenido: bytes) -> str:
    return hashlib.sha256(contenido).hexdigest()


def leer_miembro(contenido: bytes, miembro: str) -> pd.DataFrame:
    """Extrae un miembro del ZIP y lo interpreta con el formato declarado en .env."""
    with zipfile.ZipFile(io.BytesIO(contenido)) as archivo:
        nombres = archivo.namelist()
        if miembro not in nombres:
            raise KeyError(f"'{miembro}' no está en el ZIP. Contiene: {nombres}")
        with archivo.open(miembro) as fichero:
            crudo = fichero.read()
    separador = os.getenv("DATASET_SEPARATOR", "\t")
    columnas = [c.strip() for c in os.getenv("DATASET_COLUMNS", "label,text").split(",")]
    return pd.read_csv(io.BytesIO(crudo), sep=separador, header=None, names=columnas,
                       encoding=os.getenv("DATASET_ENCODING", "latin-1"), engine="python")


def main() -> int:
    if settings.data_source == "local":
        print(f"Modo local. Archivo configurado: {settings.dataset_path}")
        if settings.dataset_path.exists():
            print(f"SHA-256: {sha256(settings.dataset_path)}")
        return 0

    if settings.data_source != "url" or not settings.dataset_url:
        print("Configure DATA_SOURCE=url y DATASET_URL en .env", file=sys.stderr)
        return 2

    contenido = descargar(settings.dataset_url)
    print(f"Fuente:             {settings.dataset_url}")
    print(f"SHA-256 descargado: {huella(contenido)}")

    miembro = os.getenv("DATASET_ZIP_MEMBER", "")
    if settings.dataset_url.lower().endswith(".zip") or miembro:
        if not miembro:
            print("Configure DATASET_ZIP_MEMBER en .env", file=sys.stderr)
            return 2
        marco = leer_miembro(contenido, miembro)
        print(f"Miembro extraído:   {miembro} ({len(marco)} filas)")
        esperado = os.getenv("DATASET_EXPECTED_ROWS")
        if esperado and len(marco) != int(esperado):
            raise ValueError(f"Se esperaban {esperado} filas y llegaron {len(marco)}: "
                             "la fuente pudo haber cambiado")
        DESTINO.parent.mkdir(parents=True, exist_ok=True)
        marco.to_csv(DESTINO, index=False, encoding="utf-8")
    else:
        DESTINO.parent.mkdir(parents=True, exist_ok=True)
        DESTINO.write_bytes(contenido)

    print(f"Guardado:           {DESTINO.relative_to(ROOT)}")
    print(f"SHA-256 del CSV:    {sha256(DESTINO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
