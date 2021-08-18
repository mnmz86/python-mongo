import asyncio
from pymongo import MongoClient
from config import *


class CentroEducativo():

    '''Clase controladora del flujo de datos hacia MongoDB'''

    async def __init__(self) -> None:
        self.estado_conexion = await self.__conexion_servidor_mongodb()
    
    async def __conexion_servidor_mongodb(self): 
        try:
            cliente = await MongoClient(mongo_uri)
            db = await cliente["Evaluacion01"]
            self.__coleccion_ce = await db["CE"]
            return estado_conexion_exitoso
        except Exception as error:
            return {
                **estado_conexion_fallido, 
                respuesta:estado_conexion_fallido[respuesta] + error
            }

    async def agregar_centro_educativo(self, objeto_centro: object) -> object:
        pass
        #self.__coleccion_ce.insert_one(objeto_centro)

    async def obtener_por_codigo(self, codigo_infraestructura: int) -> object:
        centro_educativo = None
        try:
            assert type(codigo_infraestructura)==int,  "El código de infraestructura debe ser un número entero"
            assert codigo_infraestructura > 9999, "El número ingresado no es válido"
            centro_educativo = await self.__coleccion_ce.find_one({"CODIGO": codigo_infraestructura},{"_id":0})
            return {
                **devolucion_datos_exitosa,
                respuesta:[centro_educativo]
            }
        except AssertionError as error:
            return {
                **error_devolucion_datos,
                mensaje: error
            }
        except Exception as error:
            return {
                **estado_conexion_fallido, 
                respuesta:estado_conexion_fallido[respuesta] + error
            }

    async def obtener_por_nombre(self, nombre_centro_educativo:str) -> object:
        try:
            cursor = await self.__coleccion_ce.find({"NOMBRE": {"$regex":nombre_centro_educativo}},{"_id":0})
            coincidencias = await [centro_educativo for centro_educativo in cursor]
            return coincidencias
        except Exception as error:
            return {
                **estado_conexion_fallido, 
                respuesta:estado_conexion_fallido[respuesta] + error
            }

    async def obtener_por_departamento(self, codigo_departamento: int) -> list[object]:
        cursor = None
        try:
            assert type(codigo_departamento)==int,  "El código de departamento debe ser un número entero"
            assert codigo_departamento in  range(1,15), "El codigo de departamento ingresado estar desde 1 hasta 14"
            cursor = await self.__coleccion_ce.find({"DEPARTAMENTO": codigo_infraestructura},{"_id":0})
            return {
                **devolucion_generador_exitosa,
                respuesta:[cursor]
            }
        except AssertionError as error:
            return {
                **error_devolucion_datos,
                mensaje: error
            }
        except Exception as error:
            return {
                **estado_conexion_fallido, 
                respuesta:estado_conexion_fallido[respuesta] + error
            }


    async def obtener_todos(self, cantidad_a_obtener: int, cantidad_por_pagina: int = 10) -> list[object]:
        cursor = self.__coleccion_ce.find({},{"_id": 0}).batch_size(cantidad_por_pagina)
        async def funcion_generador():
            iteracion = 0
            nonlocal cantidad_a_obtener, cantidad_por_pagina, cursor
            if not cantidad_a_obtener:
                cantidad_a_obtener = self.__coleccion_ce.count()
                
            while cantidad_por_pagina*iteracion < cantidad_a_obtener:
                yield [cursor.next() for fila in range(cantidad_por_pagina)]
                iteracion += 1
            else:
                cursor.close()
        return funcion_generador

    async def actualizar_centro(self, objeto_centro: object) -> object:
        pass

    async def __obtener_departamento(self, codigo_departamento: int) -> str:
        pass

if __name__ == "__main__":
    ce = CentroEducativo()
    print(ce.estado_conexion)
    
 
    #Prueba buscar por codigo de infraestructura
    print(ce.obtener_por_codigo(0))
    print(ce.obtener_por_codigo(10001))
    print(ce.obtener_por_codigo("0"))
    print(ce.obtener_por_codigo({"$gt": 10100}))


    """ 
        #Prueba generador
        
        generador = ce.obtener_todos(30, 10)
        for i in generador():
            print (i, end="\n"*3)
    """