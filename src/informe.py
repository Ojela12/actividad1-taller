"""Funciones que generan el informe de columnas según el rol solicitado."""

from src.config import (COLUMNAS, ROLES, CRITERIOS_VALIDOS, ORDENES_VALIDOS,
                        CRITERIO_DEFECTO, ORDEN_DEFECTO)


def config_del_rol(rol=None, roles=ROLES, columnas=COLUMNAS):
    """Devuelve la configuración que corresponde a un rol.

    Args:
        rol: nombre del rol. Si es None, se usa la configuración por defecto
            (todas las columnas, por completitud, descendente).
        roles: diccionario con la definición de los roles.
        columnas: diccionario con los datos de las columnas.

    Returns:
        dict con la configuración del rol, o None si el rol no existe.
    """
    if rol is None:
        return {"columnas": list(columnas),
                "criterio": CRITERIO_DEFECTO,
                "orden": ORDEN_DEFECTO}
    return roles.get(rol)


def validar_config(config):
    """Controla criterio, orden y mínimo de una configuración de rol.

    Si algún valor es inválido (por ejemplo criterio "promedio") avisa
    por pantalla y usa el valor por defecto, para que el programa no falle.

    Args:
        config: diccionario con la configuración de un rol.

    Returns:
        tupla (criterio, orden, minimo) con valores válidos.
    """
    criterio = config.get("criterio", CRITERIO_DEFECTO)
    if criterio not in CRITERIOS_VALIDOS:
        print(f"Aviso: criterio '{criterio}' no válido, se usa '{CRITERIO_DEFECTO}'.")
        criterio = CRITERIO_DEFECTO

    orden = config.get("orden", ORDEN_DEFECTO)
    if orden not in ORDENES_VALIDOS:
        print(f"Aviso: orden '{orden}' no válido, se usa '{ORDEN_DEFECTO}'.")
        orden = ORDEN_DEFECTO

    minimo = config.get("minimo", 0)
    if minimo < 0 or minimo > 100:
        print(f"Aviso: mínimo {minimo} fuera de 0-100, no se aplica filtro.")
        minimo = 0

    return criterio, orden, minimo


def filtrar_columnas(nombres, columnas=COLUMNAS, minimo=0):
    """Deja solo las columnas que existen y cuya completitud es >= minimo.

    Args:
        nombres: lista de nombres de columnas pedidas.
        columnas: diccionario con los datos de las columnas.
        minimo: completitud mínima (0 = no filtra por completitud).

    Returns:
        lista con los nombres que cumplen la condición.
    """
    for nombre in nombres:
        if nombre not in columnas:
            print(f"Aviso: la columna '{nombre}' no existe y se ignora.")
    return list(filter(
        lambda n: n in columnas and columnas[n]["completitud"] >= minimo,
        nombres))


def ordenar_columnas(nombres, columnas=COLUMNAS, criterio=CRITERIO_DEFECTO,
                     orden=ORDEN_DEFECTO):
    """Ordena los nombres de columnas por nombre o por completitud.

    Si dos columnas tienen la misma completitud, quedan en orden alfabético
    (primero se ordena por nombre y sorted() respeta ese orden en los empates).

    Args:
        nombres: lista de nombres de columnas.
        columnas: diccionario con los datos de las columnas.
        criterio: "nombre" o "completitud".
        orden: "A" ascendente o "B" descendente.

    Returns:
        lista nueva con los nombres ordenados.
    """
    descendente = orden == "B"
    if criterio == "nombre":
        return sorted(nombres, reverse=descendente)
    return sorted(nombres, key=lambda n: columnas[n]["completitud"], reverse=descendente)



def generar_informe(rol=None, roles=ROLES, columnas=COLUMNAS):
    """Arma el informe de columnas para un rol (sin imprimir nada).

    Args:
        rol: nombre del rol, o None para informar todas las columnas.
        roles: diccionario con la definición de los roles.
        columnas: diccionario con los datos de las columnas.

    Returns:
        lista de diccionarios {"nombre", "tipo", "completitud"} en el orden
        que pide el rol. Lista vacía si el rol no existe.
    """
    config = config_del_rol(rol, roles, columnas)
    if config is None:
        print(f"Aviso: el rol '{rol}' no existe. Roles disponibles: {list(roles)}")
        return []

    criterio, orden, minimo = validar_config(config)
    filtradas = filtrar_columnas(config["columnas"], columnas, minimo)
    ordenadas = ordenar_columnas(filtradas, columnas, criterio, orden)

    return list(map(
        lambda n: {"nombre": n,
                   "tipo": columnas[n]["tipo"],
                   "completitud": columnas[n]["completitud"]},
        ordenadas))


def imprimir_informe(rol=None, roles=ROLES, columnas=COLUMNAS):
    """Imprime el informe de columnas de un rol en forma de tabla.

    Args:
        rol: nombre del rol, o None para informar todas las columnas.
        roles: diccionario con la definición de los roles.
        columnas: diccionario con los datos de las columnas.
    """
    titulo = rol if rol is not None else "sin rol (todas las columnas)"
    print(f"=== Informe: {titulo} ===")
    filas = generar_informe(rol, roles, columnas)
    if len(filas) == 0:
        print("(no hay columnas para mostrar)")
    for fila in filas:
        print(f"{fila['nombre']:12} {fila['tipo']:5} {fila['completitud']:6}%")
    print()
