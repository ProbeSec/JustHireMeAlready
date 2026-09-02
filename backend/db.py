import os
import sqlite3
import uuid
## from platformdirs import user_data_dir

def con_base_datos():
    conn = sqlite3.connect("candidaturas.db")
    return conn

# Función para inicializar la base de datos y crear la tabla si no existe
def init_db():
    conn = con_base_datos() # Ejecuta la función de conexión a la base de de datos
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS candidaturas (
            uuid TEXT PRIMARY KEY,
            estado TEXT NOT NULL CHECK (estado IN ('enviada','contactado','entrevista','oferta','rechazada','pendiente')),
            fecha_peticion TEXT NOT NULL,
            empresa TEXT NOT NULL,
            puesto TEXT NOT NULL,
            link_oferta TEXT NOT NULL,
            portal TEXT NOT NULL,
            ubicacion TEXT NOT NULL,
            modalidad TEXT NOT NULL,
            created_at TEXT,
            updated_at TEXT,
            deleted INTEGER NOT NULL DEFAULT 0
        )
        """
    )  # Ejecuta la query enviada como string para crear la tabla de candidaturas si no existe
    conn.commit()  # Aplica los cambios
    conn.close()  # Cierra la conexión a la base de datos


# Función para añadir una nueva candidatura a la base de datos
def add_candidatura(estado, fecha_peticion, empresa, puesto, link_oferta, portal, ubicacion, modalidad):
    nuevo_uuid = str(uuid.uuid4())  # Crea un nuevo uuid para la candidatura
    conn = con_base_datos() # Ejecuta la función de conexión a la base de de datos
    conn.execute(
        """
        INSERT INTO candidaturas (uuid, estado, fecha_peticion, empresa, puesto, link_oferta, portal, ubicacion, modalidad, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'), datetime('now'))
        """,
        (nuevo_uuid, estado, fecha_peticion, empresa, puesto, link_oferta, portal, ubicacion, modalidad),
    )  # Ejecuta la query enviada como string para añadir una nueva candidatura a la base de datos
    conn.commit()  # Aplica los cambios
    conn.close()  # Cierra la conexión a la base de datos

# Función para leer la base de datos
def get_all():
    conn = con_base_datos() # Ejecuta la función de conexión a la base de de datos
    cursor = conn.cursor() # Crea un cursor
    cursor.execute(
        """
        SELECT * FROM candidaturas WHERE deleted = 0
        """
    ) # Obtiene los datos de la Base de datos
    filas = cursor.fetchall() # Obtiene todos los datos y los asigna a una variable filas
    conn.close() # Cierra la conexión a la base de datos
    return filas # Devuelve los datos obtenidos de la base de datos
    
# Función para buscar una candidatura por su uuid
def get_by_id(uuid):
    conn = con_base_datos() # Ejecuta la función de conexión a la base de de datos
    cursor = conn.cursor() # Crea un cursor
    cursor.execute(
        """
        SELECT * FROM candidaturas WHERE uuid = ?
        """,
        (uuid,)
    ) # Obtiene los datos de la base de datos utilizando como filtro de búsqueda el uuid proporcionado
    candidaturaBuscada = cursor.fetchone() # Obtiene los datos y los asigna a una variable
    conn.close() # Cierra la conexión
    return candidaturaBuscada # Devuelve los datos obtenidos de la base de datos

# Función para actualizar el estado de una candidatura
def update_estado(uuid, estado):
    conn = con_base_datos() # Ejecuta la función de conexión a la base de de datos
    conn.execute (
        """
        UPDATE candidaturas SET estado = ?, updated_at = datetime('now') WHERE uuid = ?
        """,
        (estado, uuid,)
    ) # Actualiza el estado de una candidatura usando como filtro el uuid
    conn.commit() # Aplica los cambios
    conn.close() # Cierra la conexión a la base de datos

# Funcioón para actualizar una candidatura entera
def update_candidatura(uuid, estado, fecha_peticion, empresa, puesto, link_oferta, portal, ubicacion, modalidad):
    conn = con_base_datos() # Ejecuta la función de conexión a la base de de datos
    conn.execute (
        """
        UPDATE candidaturas SET estado = ?, fecha_peticion = ?, empresa = ?, puesto = ?, link_oferta = ?, portal = ?, ubicacion = ?, modalidad = ?, updated_at = datetime('now') WHERE uuid = ?
        """,
        (estado, fecha_peticion, empresa, puesto, link_oferta, portal, ubicacion, modalidad, uuid,)
    ) # Permite actualizar todos los datos de una candidatura
    conn.commit() # Aplica los cambios
    conn.close() # Cierra la conexión a la base de datos

# Función para borrar una candidatura
def soft_delete_candidatura (uuid):
    conn = con_base_datos() # Ejecuta la función de conexión a la base de de datos
    conn.execute (
        """
        UPDATE candidaturas SET deleted = 1, updated_at = datetime ('now') WHERE uuid = ?
        """,
        (uuid,)
    ) # Borra una candidatura con borrado lógico
    conn.commit() # Aplica los cambios
    conn.close () # Cierra la conexión a la base de datos


# Campo de pruebas
def test_insertar():
    add_candidatura(
        "enviada",              # estado (¡uno de los 6 del CHECK!)
        "2026-09-01",           # fecha_peticion (texto ISO)
        "Indra",                # empresa
        "SOC Analyst Junior",   # puesto
        "https://ejemplo.com",  # link_oferta
        "LinkedIn",             # portal
        "A Coruña",             # ubicacion
        "Remoto"                # modalidad
    )

    add_candidatura(
        "entrevista",              # estado (¡uno de los 6 del CHECK!)
        "2026-09-09",              # fecha_peticion (texto ISO)
        "PaloAlto",                # empresa
        "Pentester Junior",        # puesto
        "https://ejemplo.com",     # link_oferta
        "Indeed",                  # portal
        "Berlin",                  # ubicacion
        "Presencial"               # modalidad
    )

    print("Candidaturas añadidas correctamente")

def test_leer():
        candidaturas = get_all()
        for fila in candidaturas:
            print(fila)

def test_buscar():
    resultados = get_by_id("90263378-cf00-4e61-bdd3-a79bd623c7fa")
    print (f"Estos son los resultados de su búsqueda: {resultados}" )

def test_actualizar():
    update_estado("90263378-cf00-4e61-bdd3-a79bd623c7fa", "enviada")
    print ("Candidatura actualizada")
    resultados = get_by_id("90263378-cf00-4e61-bdd3-a79bd623c7fa")
    print (f"Estos son los resultados de su búsqueda: {resultados}" )

def test_actualizar_completo():
    update_candidatura(
        "90263378-cf00-4e61-bdd3-a79bd623c7fa",
        "rechazada",
        "1969-07-21",
        "NCI",
        "Cybersecurity Specialist",
        "https://modificado.com",
        "LinkedIn",
        "Madrid",
        "Presencial"
    )

    print ("Candidatura actualizada")
    resultados = get_by_id("90263378-cf00-4e61-bdd3-a79bd623c7fa")
    print (f"Estos son los resultados de su búsqueda: {resultados}" )

def test_borrado():
    soft_delete_candidatura("90263378-cf00-4e61-bdd3-a79bd623c7fa")
    print("Candidatura borrada")
    resultados = get_by_id("90263378-cf00-4e61-bdd3-a79bd623c7fa")
    print (f"Estos son los resultados de su búsqueda: {resultados}" )


# Ejecutor de pruebas
if __name__ == "__main__": 
    init_db()
    test_insertar()
    

    


