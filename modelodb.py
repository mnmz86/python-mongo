from typing import ( # Mejora las anotaciones en el código
    Iterator,
    Union, 
    Optional, 
    Callable, 
    Generator
    ) 
from config import * # Variables globales
from functools import wraps # Preserva la información de funciones, como el nombre, lo uso en gestión de errores
from pymongo import MongoClient, cursor
from pymongo.errors import (
    ConnectionFailure, 
    AutoReconnect, 
    ExecutionTimeout, 
    ServerSelectionTimeoutError, 
    OperationFailure
    )


def with_error_handler(funcion: Callable) -> Callable:

    """ Gestion de los errores en la ejecución del código """

    @wraps(funcion)
    def decorador(*args: Union[int, str, dict], **kwargs: Optional[int]) -> dict:
        try:
            # Validación de errores específicos del método
            if funcion.__name__ == "obtener_por_codigo":
                assert type(args[1])==int, causas_fallo[no_numero]
                assert args[1] > 9999, causas_fallo[numero_invalido]
            #if funcion.__name__ == "":
            #    pass
            resultado = funcion(*args, *kwargs)
            print(resultado)
            assert resultado[respuesta] != [], causas_fallo[busqueda_sin_resultados]
            return resultado
        except AssertionError as errores:
            return {
                **resultados_fallidos,
                respuesta: errores.args[0]
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
        except StopIteration as errores: # FALTA MANEJAR LOS GENERADORES
            return {
                **resultados_fallidos,
                respuesta: causas_fallo[fin_iteraciones] + "\n * ".join(errores.args)
            }
        except Exception as errores:
            return {
                **resultados_fallidos,
                respuesta: causas_fallo[otras_causas]  + "\n * ".join(errores.args)
            }
    return decorador


class CentroEducativo():

    """ Clase controladora del flujo de datos hacia MongoDB """
    
    __coleccion_ce = None

    def __init__(self) -> None:
        self.estado_conexion = self.__conexion_servidor_mongodb()

    @with_error_handler
    def __conexion_servidor_mongodb(self) -> dict:
        global __coleccion_ce # Se utiliza global porque se modificará la variable.
        cliente = MongoClient(open(".serverkey").read())
        db = cliente["Evaluacion01"]
        __coleccion_ce = db["CE"]
        return estado_conexion_exitoso

    #@with_error_handler.  FALTA REFACTORIZAR PARA QUE EL DECORADOR SOLO SE NECESITE AQUÍ Y EN OTRO PAR MÁS DE FUNCIONES
    def __ejecutar_busqueda(self, *args: Union[dict, Optional[int]]) -> dict:
        cursor = __coleccion_ce.find(args[0], {"_id":0})
        if args[0] == {}:
            return {
                **devolucion_generador_exitosa,
                respuesta: cursor.batch_size(args[1])
            }
        resultados_busqueda = list(cursor)
        return {
            **devolucion_informacion_exitosa,
            respuesta: resultados_busqueda
        }

    #@with_error_handler
    @staticmethod
    def funcion_generadora(cursor: Iterator,  cantidad_a_obtener: int, cantidad_por_pagina: int) -> Generator:
        if not cantidad_a_obtener:
            cantidad_a_obtener = __coleccion_ce.count()
        while cantidad_por_pagina < cantidad_a_obtener:
            yield [cursor.next() for fila in range(cantidad_por_pagina)]
            cantidad_a_obtener -= cantidad_por_pagina
        else:
            yield [cursor.next() for fila in range(cantidad_a_obtener)]
            cursor.close()


    @with_error_handler
    def agregar_centro_educativo(self, objeto_centro: dict) -> dict:
        resultado = __coleccion_ce.insert_one(objeto_centro)
        confirmacion = __coleccion_ce.find({"_id": resultado.inserted_id})
        return confirmacion

    @with_error_handler
    def obtener_por_codigo(self, codigo_infraestructura: int) -> dict:
        centro_educativo = self.__ejecutar_busqueda({"CODIGO": codigo_infraestructura})
        return centro_educativo

    @with_error_handler
    def obtener_por_nombre(self, nombre_centro_educativo: str) -> dict:
        centros_educativos = self.__ejecutar_busqueda({"NOMBRE": nombre_centro_educativo})
        return centros_educativos

    @with_error_handler
    def obtener_todos(self, cantidad_a_obtener: int, cantidad_por_pagina: int = 10) -> dict:
        resultado_consulta = self.__ejecutar_busqueda({}, cantidad_por_pagina)
        cursor = resultado_consulta[respuesta]
        resultado_consulta[respuesta] = CentroEducativo.funcion_generadora(cursor, cantidad_a_obtener, cantidad_por_pagina)
        return resultado_consulta

    @with_error_handler
    def actualizar_centro_educativo(self, modificacion_centro_educativo: dict) -> dict:
        resultado_busqueda = self.obtener_por_codigo({CODIGO: modificacion_centro_educativo[CODIGO]})
        centro_educativo_obtenido = resultado_busqueda[respuesta][0]
        resultado_actualizacion = __coleccion_ce.find_one_and_update(centro_educativo_obtenido, {"$set": modificacion_centro_educativo})
        del resultado_actualizacion["_id"]
        return [resultado_actualizacion]

    @with_error_handler
    def eliminar_centro_educativo(self, codigo_infraestructura: int) -> dict:
        resultado_eliminacion = __coleccion_ce.find_one_and_delete({CODIGO: codigo_infraestructura})
        return [resultado_eliminacion]



if __name__ == "__main__":
    ce = CentroEducativo()

    print(0, ce.estado_conexion)

    prueba_insert_1 = {
        CODIGO: 13095,
        NOMBRE: "CENTRO ESCOLAR NIÑO JESÚS DE PRAGA",
        DEPARTAMENTO_CENTRO: "SAN MIGUEL",
        MUNICIPIO_CENTRO: "SAN MIGUEL"
    }
    prueba_insert_2 = {
        CODIGO: 13095,
        NOMBRE: "CENTRO ESCOLAR NIÑO JESÚS DE PRAGA",
        DEPARTAMENTO_CENTRO: "SAN MIGUEL",
        MUNICIPIO_CENTRO: "SAN MIGUEL"

    }

    #ce.agregar_centro_educativo(prueba_insert_1)
    #ce.agregar_centro_educativo(prueba_insert_2)

    """
    # Prueba buscar por codigo de infraestructura
    print(1, ce.obtener_por_codigo(0))
    print(2, ce.obtener_por_codigo(10001))
    print(3, ce.obtener_por_codigo("0"))
    print(4, ce.obtener_por_codigo({"$gt": 10100}))
    print(5, ce.obtener_por_codigo(100001))
    """


    """  
    # Prueba generador
    generador = ce.obtener_todos(29, 10)[respuesta]
    
    # Versión con bucle for.
    for i in generador:
        print (i, end="\n"*3)
    """

    
    """ 
    #Versión con iterador. NO ME FUNCIONA POR LA ESTRUCTURA DE LAS RESPUESTAS IMPLEMENTADA
    generador = iter(generador)
    print(1, next(generador))
    print(2, next(generador))
    print(3,next(generador))
    print(4, next(generador))
    """