from fastapi import FastAPI          # El framework web
from pydantic import BaseModel       # Para crear modelos de datos que validan la entrada
from enum import Enum                # Para definir listas cerradas de valores válidos
import db                            # Nuestra capa de datos (db.py) con todo el SQL


# --- MODELOS DE DATOS (validación de entrada) ---

# Lista cerrada de estados válidos. Al heredar de (str, Enum), cada valor es texto
# Y solo se aceptan estos 6: cualquier otro lo rechaza FastAPI en la puerta (422).
class EstadoEnum(str, Enum):
    enviada = "enviada"
    contactado = "contactado"
    entrevista = "entrevista"
    oferta = "oferta"
    rechazada = "rechazada"
    pendiente = "pendiente"

# Modelo para CREAR/EDITAR una candidatura entera: los 8 campos que manda el cliente.
# El uuid y los timestamps NO están aquí porque los genera db.py automáticamente.
class CandidaturaNueva(BaseModel):
    estado: EstadoEnum               # Solo uno de los 6 valores del Enum
    fecha_peticion: str
    empresa: str
    puesto: str
    link_oferta: str
    portal: str
    ubicacion: str
    modalidad: str

# Modelo mínimo para cambiar SOLO el estado: no obliga a reenviar los 8 campos.
class EstadoUpdate(BaseModel):
    estado: EstadoEnum


app = FastAPI()                      # Crea la aplicación. uvicorn busca esta variable 'app'.


# --- ENDPOINTS (las URLs que expone la API) ---

# Ruta raíz: un simple "hola" para comprobar que la API responde.
@app.get("/")
def home():
    return {"mensaje": "Hola desde JustHireMeAlready"}

# GET /candidaturas -> LISTAR todas (las no borradas). Llama a get_all() de db.py.
@app.get("/candidaturas")
def listar_candidaturas():
    return db.get_all()

# POST /candidaturas -> CREAR una candidatura nueva.
# Recibe un modelo CandidaturaNueva en el cuerpo (FastAPI lo valida solo).
@app.post("/candidaturas")
def crear_candidatura(candidatura: CandidaturaNueva):
    db.add_candidatura(candidatura.estado, candidatura.fecha_peticion, candidatura.empresa,
                       candidatura.puesto, candidatura.link_oferta, candidatura.portal,
                       candidatura.ubicacion, candidatura.modalidad)
    return {"mensaje": "Candidatura añadida"}

# GET /candidaturas/{id} -> BUSCAR una sola por su uuid.
# El {id} de la URL llega como parámetro 'id' y se pasa a get_by_id().
@app.get("/candidaturas/{id}")
def buscar_candidatura(id: str):
    return db.get_by_id(id)

# PUT /candidaturas/{id} -> CAMBIAR SOLO EL ESTADO.
# Dos entradas: el 'id' (de la URL, qué candidatura) y 'datos' (del cuerpo, el nuevo estado).
@app.put("/candidaturas/{id}")
def editar_candidatura_estado(id: str, datos: EstadoUpdate):
    db.update_estado(id, datos.estado)
    return {"mensaje": "Candidatura modificada"}

# PATCH /candidaturas/{id} -> EDITAR LA CANDIDATURA COMPLETA (los 8 campos).
# 'id' de la URL + 'datos' (modelo completo) del cuerpo. Se sacan los 8 campos con punto.
@app.patch("/candidaturas/{id}")
def editar_candidatura_completa(id: str, datos: CandidaturaNueva):
    db.update_candidatura(id, datos.estado, datos.fecha_peticion, datos.empresa,
                          datos.puesto, datos.link_oferta, datos.portal,
                          datos.ubicacion, datos.modalidad)
    return {"mensaje": "Candidatura modificada totalmente"}

# DELETE /candidaturas/{id} -> BORRAR (lógico) por uuid.
# No elimina la fila, marca deleted=1 en db.py.
@app.delete("/candidaturas/{id}")
def borrar_candidatura(id: str):
    db.soft_delete_candidatura(id)
    return {"mensaje": "Candidatura eliminada"}