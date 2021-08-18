from pymongo import MongoClient
from config import mongo_uri

'''Variables globales creadas para manejar las respuestas a las peticiones y reducir
errores al escribirlas en cada respuesta, aprovechando el autocompletado'''

#Estados  de las respuestas a la interfaz
estado = "estado"
exitoso = "exitoso"
fallido = "fallido"
#Tipos de respuestas a la interfaz
tipo = "tipo"
mensaje = "mensaje"
lista = "lista"
iterador = "iterador"
#Carga últil para las respuestas
respuesta = "respuesta"

#Estados de conexion a la base de datos y devolucion de datos
estado_conexion_exitoso = {
    estado:exitoso,
    tipo:mensaje,
    respuesta: "Conexión con el servidor exitosa"
}
estado_conexion_fallido =  {
    estado:fallido,
    tipo:mensaje,
    respuesta: "No se pudo establecer una conexion con el servidor"
}
devolucion_datos_exitosa = {
    estado: exitoso,
    tipo: lista,
}
error_devolucion_datos = {
    estado:fallido,
    tipo: mensaje
}
devolucion_iterador_exitosa = {
    estado:exitoso,
    tipo:iterador
}

class CentroEducativo():

    '''Clase controladora del flujo de datos hacia MongoDB'''

    def __init__(self) -> None:
        self.estado_conexion = self.__conexion_servidor_mongodb()
    
    def __conexion_servidor_mongodb(self): 
        try:
            cliente = MongoClient(mongo_uri)
            db = cliente["Evaluacion01"]
            self.__coleccion_ce = db["CE"]
            return estado_conexion_exitoso
        except ConnectionError:
            return estado_conexion_fallido

    def agregar_centro_educativo(self, objeto_centro: object) -> object:
        pass
        #self.__coleccion_ce.insert_one(objeto_centro)

    def obtener_por_codigo(self, codigo_infraestructura: int) -> object:
        centro_educativo = None
        try:
            assert(type(codigo_infraestructura)==int)
            centro_educativo = self.__coleccion_ce.find_one({"CODIGO": codigo_infraestructura},{"_id":0})
            return {
                **devolucion_datos_exitosa,
                respuesta:[centro_educativo]
            }
        except AssertionError:
            return (
                "error",
                "mensaje",
                "Solo es posible ingresar un número entero"
            )
        except ConnectionError:
            return (
                "error",
                "mensaje",
                "Solo es posible ingresar un número entero"
            )
    def obtener_por_nombre(self, nombre_centro_educativo:str) -> object:
        try:
            cursor = self.__coleccion_ce.find({"CODIGO": {"$regex":nombre_centro_educativo}},{"_id":0})
            coincidencias = [centro_educativo for centro_educativo in cursor]
            return coincidencias
        except AssertionError:
            return "fallido", "Solo es posible ingresar un número entero"
        except ConnectionError:
            return "fallido", "Se perdió la conexión con el servidor"

    def obtener_por_departamento(self, codigo_departamento: int) -> list[object]:
        pass

    def obtener_todos(self, cantidad_a_obtener: int, cantidad_por_pagina: int = 10) -> list[object]:
        cursor = self.__coleccion_ce.find({},{"_id": 0}).batch_size(cantidad_por_pagina)
        def iterador():
            iteracion = 0
            nonlocal cantidad_a_obtener, cantidad_por_pagina, cursor
            if not cantidad_a_obtener:
                cantidad_a_obtener = self.__coleccion_ce.count()
                
            while cantidad_por_pagina*iteracion < cantidad_a_obtener:
                yield [cursor.next() for fila in range(cantidad_por_pagina)]
                iteracion += 1
            else:
                cursor.close()
        return iterador

    def actualizar_centro(self, objeto_centro: object) -> object:
        pass

    def __transaccion(self, operacion):
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
        #Prueba iterador
        
        iterador = ce.obtener_todos(30, 10)
        for i in iterador():
            print (i, end="\n"*3)
    """