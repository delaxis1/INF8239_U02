"""Configuración de la colección de pruebas.

`test_embeddings_network.py` pertenece al LAB06 y necesita gensim. En este equipo la rueda de
gensim no trae las extensiones compiladas para Python 3.12 y su importación falla, lo que
interrumpiría la colección completa. Como el Ejercicio 03 cubre LAB04 y LAB05, esa prueba se omite
de forma explícita en lugar de dejar que rompa la suite; en un entorno donde gensim cargue, se
recoge con normalidad.
"""

from __future__ import annotations

collect_ignore: list[str] = []

try:  # pragma: no cover - depende del entorno, no de la lógica del proyecto
    import gensim.models  # noqa: F401
except Exception:
    collect_ignore.append("test_embeddings_network.py")
