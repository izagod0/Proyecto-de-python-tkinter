import os
from datetime import datetime

# Nombres de archivos
ARCHIVO_CLIENTES = "clientes.txt"
ARCHIVO_HABITACIONES = "habitaciones.txt"
ARCHIVO_HISTORIAL = "historial.txt"
ARCHIVO_RESERVACIONES = "reservaciones.txt"


# ==========================================
# FUNCIONES DE ID AUTOINCREMENTAL
# ==========================================
def generar_id_autoincremental(archivo_txt):
    """Genera el siguiente ID disponible basado en los registros existentes."""
    if not os.path.exists(archivo_txt):
        return "1"

    ids_existentes = []
    with open(archivo_txt, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if datos and datos[0].isdigit():
                ids_existentes.append(int(datos[0]))

    if not ids_existentes:
        return "1"

    return str(max(ids_existentes) + 1)


def generar_id_cliente():
    """ID autoincremental para clientes con formato 001, 002..."""
    siguiente = int(generar_id_autoincremental(ARCHIVO_CLIENTES))
    return str(siguiente).zfill(3)


def generar_id_habitacion():
    """ID autoincremental para habitaciones."""
    return generar_id_autoincremental(ARCHIVO_HABITACIONES)


def generar_id_reservacion():
    """ID autoincremental para reservaciones."""
    return generar_id_autoincremental(ARCHIVO_RESERVACIONES)


# ==========================================
# FUNCIONES DE HISTORIAL
# ==========================================
def registrar_movimiento(descripcion):
    """Guarda un registro exacto de lo que pasó en el sistema."""
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(ARCHIVO_HISTORIAL, "a", encoding="utf-8") as archivo:
        archivo.write(f"{fecha_hora} | {descripcion}\n")


def obtener_historial():
    """Lee todos los movimientos para mostrarlos en la tabla."""
    if not os.path.exists(ARCHIVO_HISTORIAL):
        return []
    with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as archivo:
        return [linea.strip().split(" | ") for linea in archivo.readlines() if linea.strip()]


# ==========================================
# FUNCIONES DE CLIENTES
# ==========================================
def guardar_cliente(cliente_id, nombre, direccion, email, telefono):
    """Guarda un nuevo cliente en el archivo de texto."""
    with open(ARCHIVO_CLIENTES, "a", encoding="utf-8") as archivo:
        archivo.write(f"{cliente_id}|{nombre}|{direccion}|{email}|{telefono}\n")
    return True


def obtener_clientes():
    """Lee el archivo de clientes y devuelve una lista con los registros."""
    if not os.path.exists(ARCHIVO_CLIENTES):
        return []

    lista_clientes = []
    with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if len(datos) >= 5:
                lista_clientes.append(datos)
    return lista_clientes


def buscar_cliente_por_id(cliente_id_buscar):
    """Busca un cliente por su ID y devuelve sus datos si lo encuentra."""
    if not os.path.exists(ARCHIVO_CLIENTES):
        return None

    with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if datos[0] == str(cliente_id_buscar):
                return {
                    "id": datos[0],
                    "nombre": datos[1],
                    "direccion": datos[2],
                    "email": datos[3],
                    "telefono": datos[4]
                }
    return None


def editar_cliente(cliente_id, nombre, direccion, email, telefono):
    """Edita un cliente leyendo, modificando la línea y sobreescribiendo."""
    if not os.path.exists(ARCHIVO_CLIENTES):
        return False

    lineas_actualizadas = []
    editado = False

    with open(ARCHIVO_CLIENTES, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    for linea in lineas:
        datos = linea.strip().split("|")
        if datos[0] == str(cliente_id):
            nueva_linea = f"{cliente_id}|{nombre}|{direccion}|{email}|{telefono}\n"
            lineas_actualizadas.append(nueva_linea)
            editado = True
        else:
            lineas_actualizadas.append(linea)

    if editado:
        with open(ARCHIVO_CLIENTES, "w", encoding="utf-8") as archivo:
            archivo.writelines(lineas_actualizadas)

    return editado


# ==========================================
# FUNCIONES DE HABITACIONES
# ==========================================
def guardar_habitacion(habitacion_id, numero, estado):
    """Guarda una nueva habitación en el archivo de texto."""
    with open(ARCHIVO_HABITACIONES, "a", encoding="utf-8") as archivo:
        archivo.write(f"{habitacion_id}|{numero}|{estado}\n")
    return True


def obtener_habitaciones():
    """Lee el archivo de habitaciones y devuelve una lista con todos los registros."""
    if not os.path.exists(ARCHIVO_HABITACIONES):
        return []

    lista_habitaciones = []
    with open(ARCHIVO_HABITACIONES, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if len(datos) == 3:
                lista_habitaciones.append(datos)
    return lista_habitaciones


def editar_habitacion(hab_id, numero, estado):
    """Edita el estado o número de una habitación existente."""
    if not os.path.exists(ARCHIVO_HABITACIONES):
        return False

    lineas_actualizadas = []
    editado = False

    with open(ARCHIVO_HABITACIONES, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    for linea in lineas:
        datos = linea.strip().split("|")
        if datos[0] == str(hab_id):
            nueva_linea = f"{hab_id}|{numero}|{estado}\n"
            lineas_actualizadas.append(nueva_linea)
            editado = True
        else:
            lineas_actualizadas.append(linea)

    if editado:
        with open(ARCHIVO_HABITACIONES, "w", encoding="utf-8") as archivo:
            archivo.writelines(lineas_actualizadas)

    return editado


def obtener_habitaciones_libres():
    """Filtra y devuelve únicamente las habitaciones cuyo estado es 'Libre'."""
    todas = obtener_habitaciones()
    return [h for h in todas if h[2].lower() == "libre"]


# ==========================================
# FUNCIONES DE RESERVACIONES
# ==========================================
def guardar_reservacion(res_id, cliente, habitacion, fecha_res, hora_res, fecha_sal, costo):
    with open(ARCHIVO_RESERVACIONES, "a", encoding="utf-8") as archivo:
        archivo.write(f"{res_id}|{cliente}|{habitacion}|{fecha_res}|{hora_res}|{fecha_sal}|{costo}\n")
    return True


def obtener_reservaciones():
    """Lee el archivo de reservaciones y devuelve todos los registros."""
    if not os.path.exists(ARCHIVO_RESERVACIONES):
        return []
    with open(ARCHIVO_RESERVACIONES, "r", encoding="utf-8") as archivo:
        return [linea.strip().split("|") for linea in archivo.readlines() if linea.strip()]


def buscar_reservacion_por_id(res_id):
    """Busca una reservación por su ID."""
    if not os.path.exists(ARCHIVO_RESERVACIONES):
        return None

    with open(ARCHIVO_RESERVACIONES, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            datos = linea.strip().split("|")
            if datos[0] == str(res_id):
                return {
                    "id": datos[0],
                    "cliente": datos[1],
                    "habitacion": datos[2],
                    "fecha": datos[3],
                    "hora": datos[4],
                    "salida": datos[5],
                    "costo": datos[6]
                }
    return None


def editar_reservacion(res_id, cliente, habitacion, fecha_res, hora_res, fecha_sal, costo):
    """Edita una reservación existente."""
    if not os.path.exists(ARCHIVO_RESERVACIONES):
        return False

    lineas_actualizadas = []
    editado = False

    with open(ARCHIVO_RESERVACIONES, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    for linea in lineas:
        datos = linea.strip().split("|")
        if datos[0] == str(res_id):
            nueva_linea = f"{res_id}|{cliente}|{habitacion}|{fecha_res}|{hora_res}|{fecha_sal}|{costo}\n"
            lineas_actualizadas.append(nueva_linea)
            editado = True
        else:
            lineas_actualizadas.append(linea)

    if editado:
        with open(ARCHIVO_RESERVACIONES, "w", encoding="utf-8") as archivo:
            archivo.writelines(lineas_actualizadas)

    return editado


# ==========================================
# FUNCIÓN GENÉRICA PARA ELIMINAR
# ==========================================
def eliminar_registro(archivo_txt, id_a_eliminar):
    """Función genérica para eliminar una línea de cualquier txt buscando su ID."""
    if not os.path.exists(archivo_txt):
        return False

    con_cambios = False
    lineas_nuevas = []

    with open(archivo_txt, "r", encoding="utf-8") as f:
        lineas = f.readlines()

    for linea in lineas:
        datos = linea.strip().split("|")
        if datos[0] != str(id_a_eliminar):
            lineas_nuevas.append(linea)
        else:
            con_cambios = True

    if con_cambios:
        with open(archivo_txt, "w", encoding="utf-8") as f:
            f.writelines(lineas_nuevas)

    return con_cambios