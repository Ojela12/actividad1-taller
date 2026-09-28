"""Configuración del ejercicio: datos de las columnas y definición de roles.

Este archivo tiene solamente DATOS, nada de lógica. Si cambia una columna
o un rol, se modifica acá y no hace falta tocar src/informe.py.
"""

COLUMNAS = {
    "PONDERA":    {"tipo": "int", "completitud": 100},
    "ESTADO":     {"tipo": "int", "completitud": 100},
    "CAT_OCUP":   {"tipo": "int", "completitud": 58.3},
    "EDAD":       {"tipo": "int", "completitud": 99.6},
    "REGION":     {"tipo": "int", "completitud": 100},
    "AGLOMERADO": {"tipo": "int", "completitud": 100},
    "ANO4":       {"tipo": "int", "completitud": 100},
    "TRIMESTRE":  {"tipo": "int", "completitud": 100},
    "ITF":        {"tipo": "int", "completitud": 84.7},
    "MAS_500":    {"tipo": "bool", "completitud": 100},
    "GDECCFR":    {"tipo": "int", "completitud": 84.7},
}

ROLES = {
    "docente": {
        "columnas": ["ESTADO", "CAT_OCUP", "EDAD", "REGION", "AGLOMERADO", "MAS_500"],
        "criterio": "nombre",
        "orden": "A",
    },
    "investigador": {
        "columnas": ["PONDERA", "ESTADO", "CAT_OCUP", "EDAD", "ITF", "GDECCFR", "ANO4", "TRIMESTRE"],
        "criterio": "completitud",
        "orden": "B",
        "minimo": 80,
    },
    "analista": {
        "columnas": ["PONDERA", "ESTADO", "CAT_OCUP", "ITF", "GDECCFR", "REGION", "AGLOMERADO"],
        "criterio": "completitud",
        "orden": "A",
    },
    "economista": {
        "columnas": ["PONDERA", "ESTADO", "CAT_OCUP", "REGION", "AGLOMERADO","ANO4", "TRIMESTRE", "ITF", "GDECCFR"],
        "criterio": "nombre",
        "orden": "A",
        "minimo": 90,
    },
}

CRITERIOS_VALIDOS = ("nombre", "completitud")
ORDENES_VALIDOS = ("A", "B")
CRITERIO_DEFECTO = "completitud"
ORDEN_DEFECTO = "B"
