from _typeshed import NoneType
from typing import Union
from config import *
from functools import wraps # Preserva la información de funciones, como el nombre, lo uso en gestión de errores
from pymongo import MongoClient
from pymongo.errors import (
    ConnectionFailure, 
    AutoReconnect, 
    ExecutionTimeout, 
    ServerSelectionTimeoutError, 
    OperationFailure)

def transaccion(funcion: object) -> object:
    @wraps(funcion)
    def decorador(*args: Union[int, str, dict], **kwargs: int) -> object:
        try:
            if funcion.__name__ == "obtener_por_codigo":
                assert type(args[1])==int, causas_fallo[no_numero]
                assert args[1] > 9999, causas_fallo[numero_invalido]
            if function.__name__ == ""
            resultado = funcion(*args, *kwargs)
            return resultado
        except AssertionError as error:
            return {
                **resultados_fallidos,
                mensaje: error.args[0]
            }
        except (AutoReconnect, ConnectionFailure) as errores:
            return {
                **resultados_fallidos, 
                respuesta: causas_fallo[conexion_fallida] + "\n * ".join(errores.args)
            }
        except (ExecutionTimeout, ServerSelectionTimeoutError) as errores:
            return {
                **resultados_fallidos, 
                respuesta: causas_fallo[tiempo_excedido] + "\n * ".join(errores.args)
            }
        except OperationFailure as errores:
            return {
                **resultados_fallidos,
                respuesta: causas_fallo[peticiones_incorrectas]  + "\n * ".join(errores.args)
            }
        except Exception as errores:
            return {
                **resultados_fallidos,
                respuesta: causas_fallo[otras_causas]  + "\n * ".join(errores.args)
            }
    return decorador


class CentroEducativo():

    '''Clase controladora del flujo de datos hacia MongoDB'''

    def __init__(self) -> None:
        self.estado_conexion = self.__conexion_servidor_mongodb()
        
    @transaccion
    def __conexion_servidor_mongodb(self): 
        cliente = MongoClient(open(".serverkey").read())
        db = cliente["Evaluacion01"]
        self.__coleccion_ce = db["CE"]
        return estado_conexion_exitoso

    @transaccion
    def agregar_centro_educativo(self, objeto_centro: dict) -> dict:
        pass
        #self.__coleccion_ce.insert_one(objeto_centro)

    @transaccion
    def obtener_por_codigo(self, codigo_infraestructura: int) -> object:
        centro_educativo = self.__coleccion_ce.find_one({"CODIGO": codigo_infraestructura},{"_id":0})
        return {
            **devolucion_informacion_exitosa,
            respuesta:[centro_educativo]
        }

    @transaccion
    def obtener_por_nombre(self, nombre_centro_educativo: str) -> object:
        cursor = self.__coleccion_ce.find({"NOMBRE": {"$regex":nombre_centro_educativo}},{"_id":0})
        coincidencias = [centro_educativo for centro_educativo in cursor]
        return coincidencias

    @transaccion
    def obtener_todos(self, cantidad_a_obtener: int, cantidad_por_pagina: int = 10) -> list[object]:
        cursor = self.__coleccion_ce.find({},{"_id": 0}).batch_size(cantidad_por_pagina)
        def funcion_generador():
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

    @transaccion
    def actualizar_centro(self, objeto_centro: object) -> object:
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