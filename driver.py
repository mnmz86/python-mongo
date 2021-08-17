import collections
from re import findall
from pymongo import MongoClient
from config import mongo_uri

class CentroEscolar():
    '''Clase controladora del flujo de datos hacia MongoDB'''
    client = MongoClient(mongo_uri)
    db = client["Evaluuacion01"]
    ce = db["CE"]

    def __init__(self) -> None:
        pass

    def agregar_centro(self, objeto_centro: object) -> object:
        pass

    def buscar_por_codigo(self, codigo_infraestructura: int) -> object:
        pass

    def buscar_por_nombre(self, nombre:str) -> object:
        pass

    def mostrar_por_departamento(self, codigo_departamento: int) -> list[object]:
        pass

    def mostrar_todos(self) -> list[object]:
        pass

    def actualizar_centro(self, objeto_centro: object) -> object:
        pass

    def __transaccion(self, operacion):
        pass

