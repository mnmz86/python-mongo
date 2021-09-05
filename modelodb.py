from threading import local
from typing import ( # Mejora las anotaciones en el código
    Iterator,
    Union, 
    Optional, 
    Callable, 
    Generator
    )
from configuracion import( # Variables globales
    ConfiguracionDB as DB,
    ErroresPrevistos as Error,
    AtributosCentroEscolar as CE,
    Respuestas as Resp
    )
from functools import wraps # Preserva la información de funciones, como el nombre, lo uso en gestión de errores
from pymongo import MongoClient, ASCENDING
from pymongo.errors import (
    ConnectionFailure, 
    AutoReconnect, 
    ExecutionTimeout, 
    ServerSelectionTimeoutError, 
    OperationFailure
    )



def con_gestion_de_errores(funcion: Callable) -> Callable:

    """ Gestion de los errores en la ejecución del código """

    @wraps(funcion)
    def decorador(*args: Union[int, str, dict], **kwargs: Optional[int]) -> dict:
        try:
            resultado = funcion(*args, *kwargs)
            return resultado
        except AssertionError as error:
            return Resp.resultados_fallidos("Error en los datos.", error)

        except (AutoReconnect, ConnectionFailure) as error:
            return Resp.resultados_fallidos(Error.CONEXION_FALLIDA, error)

        except (ExecutionTimeout, ServerSelectionTimeoutError) as error:
            return Resp.resultados_fallidos(Error.TIEMPO_EXCEDIDO, error)

        except OperationFailure as error:
            return Resp.resultados_fallidos(Error.PETICIONES_INCORRECTAS, error)

        except StopIteration as error: # FALTA MANEJAR LOS GENERADORES
            return Resp.resultados_fallidos(Error.FIN_ITERACIONES, error)

        except KeyError as error:
            return Resp.resultados_fallidos(Error.FUERA_DE_RANGO, error)

        except ValueError as error:
            return Resp.resultados_fallidos(Error.NO_ES_NUMERO, error)

        except Exception as error:
            return Resp.resultados_fallidos(Error.OTRAS_CAUSAS, error)

    return decorador


class CentroEducativo():

    """ Clase controladora del flujo de datos hacia MongoDB """
    
    __coleccion_ce = None

    def __init__(self) -> None:
        self.estado_conexion = self.__conexion_servidor_mongodb()

    @con_gestion_de_errores
    def __conexion_servidor_mongodb(self) -> dict:
        global __coleccion_ce # Se utiliza global porque se modificará la variable.
        cliente = MongoClient(DB.URI)
        db = cliente[DB.DB]
        __coleccion_ce = db[DB.COLECCION]
        #La primera vez, para ejecutar búsquedas
        indices_busqueda = __coleccion_ce.index_information()
        cadena_indices = ",".join(indices_busqueda.keys()) # Se unen como cadenas porque Mongo le concatena el tipo de índice como parte del nombre
        v = None
        if CE.CODIGO not in cadena_indices or CE.NOMBRE not in cadena_indices:
            from vista import Visualizador
            v = Visualizador()
        if CE.CODIGO not in cadena_indices: 
            respuesta_indice_CODIGO = __coleccion_ce.create_index([(CE.CODIGO, ASCENDING)], unique=True)
            respuesta_indice_CODIGO = Resp.preparar_respuesta(
                Resp.EXITOSO, Resp.MENSAJE, 
                (
                    "Se creó el índice de búsqueda para " + CE.CODIGO,
                    respuesta_indice_CODIGO
                )
            )
            v.visualizar_mensaje(respuesta_indice_CODIGO)
            
        if CE.NOMBRE not in cadena_indices:
            respuesta_indice_NOMBRE = __coleccion_ce.create_index([(CE.NOMBRE, 'text')])
            respuesta_indice_NOMBRE = Resp.preparar_respuesta(
                Resp.EXITOSO, Resp.MENSAJE, 
                (
                    "Se creó el índice de búsqueda para " + CE.CODIGO,
                    respuesta_indice_NOMBRE
                )
            )
            v.visualizar_mensaje(respuesta_indice_NOMBRE)

            del v, Visualizador

        return Resp.estado_conexion_exitoso()

    def __ejecutar_busqueda(self, *args: Union[dict, Optional[int]]) -> dict:
        cursor = __coleccion_ce.find(args[0], {"_id":0})
        resultados_busqueda = list(cursor)
        cursor.close()
        return Resp.devolucion_informacion_exitosa(resultados_busqueda)

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


    @con_gestion_de_errores #REVISADO
    def agregar_centro_educativo(self, objeto_centro: dict) -> dict:
        revision_coincidencias = __coleccion_ce.find_one(objeto_centro)
        assert revision_coincidencias == None, Error.PETICIONES_INCORRECTAS \
            + "\nSe encontró un documento con este nombre"
        resultado = __coleccion_ce.insert_one(objeto_centro)
        confirmacion = __coleccion_ce.find({"_id": resultado.inserted_id}, {"_id": 0})
        confirmacion = list(confirmacion)
        return Resp.devolucion_informacion_exitosa(confirmacion)

    @con_gestion_de_errores #REVISADO
    def obtener_por_codigo(self, codigo_infraestructura: int) -> dict:
        codigo_infraestructura = int(codigo_infraestructura)
        assert codigo_infraestructura > 9999, Error.FUERA_DE_RANGO
        centro_educativo = self.__ejecutar_busqueda({CE.CODIGO: int(codigo_infraestructura)})
        return centro_educativo

    @con_gestion_de_errores #REVISADO
    def obtener_por_nombre(self, nombre_centro_educativo: str) -> dict:
        assert "{" not in nombre_centro_educativo, Error.CARACTER_NO_VALIDO
        assert "$" not in nombre_centro_educativo, Error.CARACTER_NO_VALIDO
        diccionario_busqueda = {
            "$text": {
                "$search": nombre_centro_educativo,
                "$language": "spanish",
                "$caseSensitive": False,
                "$diacriticSensitive": False
                }
            }
        centros_educativos = self.__ejecutar_busqueda(diccionario_busqueda)
        return centros_educativos

    @con_gestion_de_errores #REVISADO
    def obtener_todos(self, cantidad_a_obtener: int, cantidad_por_pagina: int = 10) -> dict:
        cantidad_a_obtener = int(cantidad_a_obtener)
        cantidad_por_pagina = int(cantidad_por_pagina)
        cursor = __coleccion_ce.find({}, {"_id":0}).batch_size(cantidad_por_pagina)
        funcion_generadora: Iterator = CentroEducativo.funcion_generadora(cursor, cantidad_a_obtener, cantidad_por_pagina)
        return Resp.devolucion_generador_exitosa(funcion_generadora)

    @con_gestion_de_errores #REVISADO
    def actualizar_centro_educativo(self, modificacion_centro_educativo: dict) -> dict:
        resultado_busqueda = self.obtener_por_codigo({CE.CODIGO: modificacion_centro_educativo[CE.CODIGO]})
        centro_educativo_obtenido = resultado_busqueda[Resp.CONTENIDO][0]
        resultado_actualizacion = __coleccion_ce.find_one_and_update(centro_educativo_obtenido, {"$set": modificacion_centro_educativo})
        del resultado_actualizacion["_id"]
        return [resultado_actualizacion]

    @con_gestion_de_errores #REVISADO
    def eliminar_centro_educativo(self, codigo_infraestructura: int) -> dict:
        codigo_infraestructura = int(codigo_infraestructura)
        assert codigo_infraestructura > 10000,  Error.FUERA_DE_RANGO
        resultado_eliminacion = __coleccion_ce.find_one_and_delete({CE.CODIGO: codigo_infraestructura}, {"_id":0})
        return Resp.devolucion_informacion_exitosa([resultado_eliminacion])


class TestModeloDB:
    """Pruebas de conexion a BD"""
    
    ce = CentroEducativo()

    def test_EstadoConexion():
        
        from vista import Visualizador
        v = Visualizador()
        v.visualizar_mensaje(TestModeloDB.ce.estado_conexion)
        
        print(TestModeloDB.ce.estado_conexion)

    def  test_AgregarYBuscarCE():
        prueba_insert_1 = {
            CE.CODIGO: 13095,
            CE.NOMBRE: "CENTRO ESCOLAR NIÑO JESÚS DE PRAGA",
            CE.DEPARTAMENTO_CENTRO: "SAN MIGUEL",
            CE.MUNICIPIO_CENTRO: "SAN MIGUEL"
        }
        print(TestModeloDB.ce.agregar_centro_educativo(prueba_insert_1))
        print(TestModeloDB.ce.obtener_por_nombre(prueba_insert_1[CE.NOMBRE]))

    def test_ElimninarCE():
        print(TestModeloDB.ce.eliminar_centro_educativo("13095"))
    
    def  test_BuscarPorCodigo():
        """Prueba buscar por codigo de infraestructura"""
        print(1, TestModeloDB.ce.obtener_por_codigo(0))
        print(2, TestModeloDB.ce.obtener_por_codigo(10001))
        print(3, TestModeloDB.ce.obtener_por_codigo("0"))
        print(4, TestModeloDB.ce.obtener_por_codigo({"$gt": 10100}))
        print(5, TestModeloDB.ce.obtener_por_codigo(100001))


    def test_Generador():
        """Prueba generador """
        generador = TestModeloDB.ce.obtener_todos(29,10)[Resp.CONTENIDO]
        # Versión con bucle for.
        """
        from vista import Visualizador
        vista = Visualizador()
        """
        for lista_centros in generador:
            #vista.visualizar_lista_centros(lista_centros)
            print (lista_centros, end="\n"*3)



if __name__ == "__main__":
    #TestModeloDB.test_EstadoConexion()
    #TestModeloDB.test_Generador()
    


    
    """ 
    #Versión con iterador. NO ME FUNCIONA POR LA ESTRUCTURA DE LAS RESPUESTAS IMPLEMENTADA
    generador = iter(generador)
    print(1, next(generador))
    print(2, next(generador))
    print(3,next(generador))
    print(4, next(generador))
    """