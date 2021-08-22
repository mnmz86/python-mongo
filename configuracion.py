from  collections import OrderedDict
import collections
from typing import Callable, MutableMapping
from pymongo.errors import (
    ConnectionFailure,
    AutoReconnect,
    ExecutionTimeout,
    ServerSelectionTimeoutError,
    OperationFailure
    )

class AtributosCentroEscolar:
    '''
    Elementos que se almacenan de un centro educativo.
    '''

    CODIGO = "CODIGO"
    NOMBRE = "NOMBRE"
    DEPARTAMENTO_CENTRO = "DEPARTAMENTO_CENTRO"
    MUNICIPIO_CENTRO = "MUNICIPIO_CENTRO"

    obtener_como_objeto: Callable[[], dict] = lambda: {
        AtributosCentroEscolar.CODIGO: 0,
        AtributosCentroEscolar.NOMBRE: "",
        AtributosCentroEscolar.DEPARTAMENTO_CENTRO: "",
        AtributosCentroEscolar.MUNICIPIO_CENTRO: ""
    }


class UbicacionCentroEscolar():
    '''
    Códigos de departamentos y municipios.
    '''

    LISTA_DEPARTAMENTOS =  {1: 'AHUACHAPÁN', 2: 'SANTA ANA', 3: 'SONSONATE', 4: 'CHALATENANGO', 5: 'LA LIBERTAD', 6: 'SAN SALVADOR', 7: 'CUSCATLÁN', 8: 'LA PAZ', 9: 'CABAÑAS', 10: 'SAN VICENTE', 11: 'USULUTÁN', 12: 'SAN MIGUEL', 13: 'MORAZÁN', 14: 'LA UNIÓN'}
    LISTA_MUNICIPIOS = {101: 'AHUACHAPÁN', 102: 'APANECA', 103: 'ATIQUIZAYA', 104: 'CONCEPCIÓN DE ATACO', 105: 'EL REFUGIO', 106: 'GUAYMANGO', 107: 'JUJUTLA', 108: 'SAN FRANCISCO MENÉNDEZ', 109: 'SAN LORENZO', 110: 'SAN PEDRO PUXTLA', 111: 'TACUBA', 112: 'TURÍN', 201: 'CANDELARIA DE LA FRONTERA', 202: 'COATEPEQUE', 203: 'CHALCHUAPA', 204: 'EL CONGO', 205: 'EL PORVENIR', 206: 'MASAHUAT', 207: 'METAPAN', 208: 'SAN ANTONIO PAJONAL', 209: 'SAN SEBASTIÁN SALITRILLO', 210: 'SANTA ANA', 211: 'SANTA ROSA GUACHIPILÍN', 212: 'SANTIAGO DE LA FRONTERA', 213: 'TEXISTEPEQUE', 301: 'ACAJUTLA', 302: 'ARMENIA', 303: 'CALUCO', 304: 'CUISNAHUAT', 305: 'SANTA ISABEL ISHUATÁN', 306: 'IZALCO', 307: 'JUAYUA', 308: 'NAHUIZALCO', 309: 'NAHULINGO', 310: 'SALCOATITÁN', 311: 'SAN ANTONIO DEL MONTE', 312: 'SAN JULIÁN', 313: 'SANTA CATARINA MASAHUAT', 314: 'SANTO DOMINGO DE GUZMÁN', 315: 'SONSONATE', 316: 'SONZACATE', 401: 'AGUA CALIENTE', 402: 'ARCATAO', 403: 'AZACUALPA', 404: 'CITALÁ', 405: 'COMALAPA', 406: 'CONCEPCIÓN QUEZALTEPEQUE', 407: 'CHALATENANGO', 408: 'DULCE NOMBRE DE MARÍA', 409: 'EL CARRIZAL', 410: 'EL PARAISO', 411: 'LA LAGUNA', 412: 'LA PALMA', 413: 'LA REINA', 414: 'LAS VUELTAS', 415: 'NOMBRE DE JESÚS', 416: 'NUEVA CONCEPCIÓN', 417: 'NUEVA TRINIDAD', 418: 'OJOS DE AGUA', 419: 'POTONICO', 420: 'SAN ANTONIO DE LA CRUZ', 421: 'SAN ANTONIO LOS RANCHOS', 422: 'SAN FERNANDO', 423: 'SAN FRANCISCO LEMPA', 424: 'SAN FRANCISCO MORAZÁN', 425: 'SAN IGNACIO', 426: 'SAN ISIDRO LABRADOR', 427: 'CANCASQUE', 428: 'LAS FLORES', 429: 'SAN LUIS DEL CARMEN', 430: 'SAN MIGUEL DE MERCEDES', 431: 'SAN RAFAEL', 432: 'SANTA RITA', 433: 'TEJUTLA', 501: 'ANTIGUO CUSCATLÁN', 502: 'CIUDAD ARCE', 503: 'COLÓN', 504: 'COMASAGUA', 505: 'CHILTIUPÁN', 506: 'HUIZUCAR', 507: 'JAYAQUE', 508: 'JICALAPA', 509: 'LA LIBERTAD', 510: 'NUEVO CUSCATLÁN', 511: 'SANTA TECLA', 512: 'QUEZALTEPEQUE', 513: 'SACACOYO', 514: 'SAN JOSÉ VILLANUEVA', 515: 'SAN JUAN OPICO', 516: 'SAN MATÍAS', 517: 'SAN PABLO TACACHICO', 518: 'TAMANIQUE', 519: 'TALNIQUE', 520: 'TEOTEPEQUE', 521: 'TEPECOYO', 522: 'ZARAGOZA', 601: 'AGUILARES', 602: 'APOPA', 603: 'AYUTUXTEPEQUE', 604: 'CUSCATANCINGO', 605: 'EL PAISNAL', 606: 'GUAZAPA', 607: 'ILOPANGO', 608: 'MEJICANOS', 609: 'NEJAPA', 610: 'PANCHIMALCO', 611: 'ROSARIO DE MORA', 612: 'SAN MARCOS', 613: 'SAN MARTÍN', 614: 'SAN SALVADOR', 615: 'SANTIAGO TEXACUANGOS', 616: 'SANTO TOMAS', 617: 'SOYAPANGO', 618: 'TONACATEPEQUE', 619: 'DELGADO', 701: 'CANDELARIA', 702: 'COJUTEPEQUE', 703: 'EL CARMEN', 704: 'EL ROSARIO', 705: 'MONTE SAN JUAN', 706: 'ORATORIO DE CONCEPCIÓN', 707: 'SAN BARTOLOME PERULAPÍA', 708: 'SAN CRISTOBAL', 709: 'SAN JOSÉ GUAYABAL', 710: 'SAN PEDRO PERULAPÁN', 711: 'SAN RAFAEL CEDROS', 712: 'SAN RAMÓN', 713: 'SANTA CRUZ ANALQUITO', 714: 'SANTA CRUZ MICHAPA', 715: 'SUCHITOTO', 716: 'TENANCINGO', 801: 'CUYULTITÁN', 802: 'EL ROSARIO', 803: 'JERUSALÉN', 804: 'MERCEDES LA CEIBA', 805: 'OLOCUILTA', 806: 'PARAISO DE OSORIO', 807: 'SAN ANTONIO MASAHUAT', 808: 'SAN EMIGDIO', 809: 'SAN FRANCISCO CHINAMECA', 810: 'SAN JUAN NONUALCO', 811: 'SAN JUAN TALPA', 812: 'SAN JUAN TEPEZONTES', 813: 'SAN LUIS TALPA', 814: 'SAN MIGUEL TEPEZONTES', 815: 'SAN PEDRO MASAHUAT', 816: 'SAN PEDRO NONUALCO', 817: 'SAN RAFAEL OBRAJUELO', 818: 'SANTA MARÍA OSTUMA', 819: 'SANTIAGO NONUALCO', 820: 'TAPALHUACA', 821: 'ZACATECOLUCA', 822: 'SAN LUIS LA HERRADURA', 901: 'CINQUERA', 902: 'GUACOTECTI', 903: 'ILOBASCO', 904: 'JUTIAPA', 905: 'SAN ISIDRO', 906: 'SENSUNTEPEQUE', 907: 'TEJUTEPEQUE', 908: 'VICTORIA', 909: 'VILLA DOLORES', 1001: 'APASTEPEQUE', 1002: 'GUADALUPE', 1003: 'SAN CAYETANO ISTEPEQUE', 1004: 'SANTA CLARA', 1005: 'SANTO DOMINGO', 1006: 'SAN ESTEBAN CATARINA', 1007: 'SAN ILDEFONSO', 1008: 'SAN LORENZO', 1009: 'SAN SEBASTIÁN', 1010: 'SAN VICENTE', 1011: 'TECOLUCA', 1012: 'TEPETITÁN', 1013: 'VERAPAZ', 1101: 'ALEGRÍA', 1102: 'BERLÍN', 1103: 'CALIFORNIA', 1104: 'CONCEPCIÓN BATRES', 1105: 'EL TRIUNFO', 1106: 'EREGUAYQUÍN', 1107: 'ESTANZUELAS', 1108: 'JIQUILISCO', 1109: 'JUCUAPA', 1110: 'JUCUARÁN', 1111: 'MERCEDES UMAÑA', 1112: 'NUEVA GRANADA', 1113: 'OZATLÁN', 1114: 'PUERTO EL TRIUNFO', 1115: 'SAN AGUSTÍN', 1116: 'SAN BUENA VENTURA', 1117: 'SAN DIONISIO', 1118: 'SANTA ELENA', 1119: 'SAN FRANCISCO JAVIER', 1120: 'SANTA MARÍA', 1121: 'SANTIAGO DE MARÍA', 1122: 'TECAPÁN', 1123: 'USULUTÁN', 1201: 'CAROLINA', 1202: 'CIUDAD BARRIOS', 1203: 'COMACARÁN', 1204: 'CHAPELTIQUE', 1205: 'CHINAMECA', 1206: 'CHIRILAGUA', 1207: 'EL TRÁNSITO', 1208: 'LOLOTIQUE', 1209: 'MONCAGUA', 1210: 'NUEVA GUADALUPE', 1211: 'NUEVO EDÉN DE SAN JUAN', 1212: 'QUELEPA', 1213: 'SAN ANTONIO', 1214: 'SAN GERARDO', 1215: 'SAN JORGE', 1216: 'SAN LUIS DE LA REINA', 1217: 'SAN MIGUEL', 1218: 'SAN RAFAEL ORIENTE', 1219: 'SESORI', 1220: 'ULUAZAPA', 1301: 'ARAMBALA', 1302: 'CACAOPERA', 1303: 'CORINTO', 1304: 'CHILANGA', 1305: 'DELICIAS DE CONCEPCIÓN', 1306: 'EL DIVISADERO', 1307: 'EL ROSARIO', 1308: 'GUALOCOCTI', 1309: 'GUATAJIAGA', 1310: 'JOATECA', 1311: 'JOCOAITIQUE', 1312: 'JOCORO', 1313: 'LOLOTIQUILLO', 1314: 'MEANGUERA', 1315: 'OSICALA', 1316: 'PERQUÍN', 1317: 'SAN CARLOS', 1318: 'SAN FERNANDO', 1319: 'SAN FRANCISCO GOTERA', 1320: 'SAN ISIDRO', 1321: 'SAN SIMÓN', 1322: 'SENSEMBRA', 1323: 'SOCIEDAD', 1324: 'TOROLA', 1325: 'YAMABAL', 1326: 'YOLOAIQUÍN', 1401: 'ANAMORÓS', 1402: 'BOLÍVAR', 1403: 'CONCEPCIÓN DE ORIENTE', 1404: 'CONCHAGUA', 1405: 'EL CARMEN', 1406: 'EL SAUCE', 1407: 'INTIPUCÁ', 1408: 'LA UNIÓN', 1409: 'LISLIQUE', 1410: 'MEANGUERA DEL GOLFO', 1411: 'NUEVA ESPARTA', 1412: 'PASAQUINA', 1413: 'POLORÓS', 1414: 'SAN ALEJO', 1415: 'SAN JOSÉ', 1416: 'SANTA ROSA DE LIMA', 1417: 'YAYANTIQUE', 1418: 'YUCUAIQUÍN'}

    #Devuelve diccionario con departamento y municipio
    obtener_ubicacion: Callable[[str], dict] = lambda codigo: {
        AtributosCentroEscolar.DEPARTAMENTO_CENTRO: UbicacionCentroEscolar.LISTA_DEPARTAMENTOS[int(codigo[:-2])],
        AtributosCentroEscolar.MUNICIPIO_CENTRO: UbicacionCentroEscolar.LISTA_MUNICIPIOS[int(codigo[:])]
        }


class ErroresPrevistos:
    '''
    Estados de conexion a la base de datos y devolucion de datos

    '''

    CONEXION_FALLIDA = "No se pudo establecer una conexion con el servidor."
    TIEMPO_EXCEDIDO = "El límite de tiempo de espera ha sido excedido."
    PETICIONES_INCORRECTAS = "Falló la operación requerida."
    FIN_ITERACIONES = "Ha llegado al final de las iteraciones."
    NO_ES_NUMERO = "Debe ingresar un número entero en este campo."
    FUERA_DE_RANGO = "El valor ingresado en el campo no está dentro del rango permitido"
    BUSQUEDA_SIN_RESULTADOS = "No se han encontrado resultados de búsqueda con la información proporcionada."
    OTRAS_CAUSAS = "Error en el servidor."

    # Para listar detalles, donde aplique.
    detalles: Callable[[Exception], str] = lambda error:  ("\n  Posible(s) causa(s):\n * " + "\n * ".join(error.args)) if len(error.args) > 0 else ""

    # Exitos


class EstilosImpresionCaracteres:
    '''
    Códigos de estilos para mostrar en pantalla.
    Se pueden combinar en la clase concatenando con el texto o usando el método "mix_estilos"
    de la siguiente forma:
        mix_estilos("NEGRITA", "CURSIVA", "INVERTIR") Mostraría estilo negrita, cursiva y
        orden de color fondo-caracter invertidos
    Si los valores no coiniden con las claves disponibles, se levantará una excepción KeyError.
    '''

    NORMAL =    '\033[0m' #Devuelve al estado original cualquier modificación
    NEGRITA =   '\033[1m'
    CURSIVA =   '\033[3m'
    SUBRAYADO = '\033[4m'
    INVERTIR =  '\033[7m' #Fondo y texto cambian colores
    SOMBRA =    '\033[8m' #Solo se ve la letra del cursor
    TACHADO =   '\033[9m'

    # Devuelve estilos mezclados
    mix_estilos: Callable[[tuple], str] = lambda *estilos: "".join([EstilosImpresionCaracteres.__dict__[i] for i in estilos])


class __CodigosColores:
    '''
    Clase que heredan  las regiones y caracteres a colorear.
    '''

    #Colores: es el ultimo dígito
    D = 0 #NEGRO
    R = 1 #ROJO
    G = 2 #VERDE
    Y = 3 #AMARILLO
    B = 4 #AZUL
    M = 5 #MAGENTA
    C = 6 #CIAN
    W = 7 #BLANCO

    # Región a colorear
    CARACTER = 3
    FONDO = 4
    #CARACTER_CLARO = 9
    #FONDO_CLARO = 10


def __obtener_codigos(texto_o_fondo: int) -> tuple:
    lista_codigos = []
    for (k, v) in OrderedDict(__CodigosColores.__dict__).items():
        if len(k)==1:
            codigo = texto_o_fondo * 10 + v
            codigo = f'\033[{codigo}m'
            lista_codigos.append(codigo)
    print(*lista_codigos)
    return lista_codigos

class ColoresImpresionDisponibles:
    '''
    Colores, regiones a colorear y tonalidades disponibles. Usan la primera letra en inglés,
    salvo el negro, que para no confundir (la B de "black") con la B de "blue" (en ingles)
    se usó la letra D (por Dark xD).
    Se usan enteros para combinar de la siguiente manera:
        Si se requiere...
        > Texto azul : CARACTER*10 + B
        > Fondo rojo: FONDO*10 + R
        > Texto negro claro: FONDO_CLARO*10 + D
    '''

    
    class CARACTER(__CodigosColores):
        D, R, G, Y, B, M, G, W = __obtener_codigos(__CodigosColores.CARACTER)
    class F0ND0:
        D, R, G, Y, B, M, G, W = __obtener_codigos(__CodigosColores.FONDO)



'''
Variables globales creadas para manejar las respuestas a las peticiones y reducir
errores al escribirlas en cada respuesta, aprovechando el autocompletado
'''
# Estados  de las respuestas a la interfaz
estado = "estado"
exitoso = "exitoso"
fallido = "fallido"
# Tipos de respuestas a la interfaz
tipo_respuesta = "tipo_respuesta"
mensaje = "mensaje"
lista = "lista"
generador = "generador"
# Carga últil para las respuestas
respuesta = "respuesta"

estado_conexion_exitoso = {
    estado:exitoso,
    tipo_respuesta:mensaje,
    respuesta: "Conexión con el servidor exitosa."
}
devolucion_informacion_exitosa = {
    estado: exitoso,
    tipo_respuesta: lista
}
devolucion_generador_exitosa = {
    estado:exitoso,
    tipo_respuesta:generador
}
    # Fracasos
resultados_fallidos = {
    estado:fallido,
    tipo_respuesta: mensaje
}




if __name__=="__main__":
    #Pruebas
    def tests():

        print(AtributosCentroEscolar.obtener_como_objeto())


        print(UbicacionCentroEscolar.LISTA_DEPARTAMENTOS)
        print(UbicacionCentroEscolar.obtener_ubicacion('1123'))


        print(ErroresPrevistos.FIN_ITERACIONES)
        class argumento_error0:
            args = ()
        print(ErroresPrevistos.detalles(argumento_error0))
        for i in range(1,4):
            class argumento_error:
                if i%2:
                    args = ("Blah "*i,)
                else:
                    args = tuple(["Blah" for j in range(i)])
            print(ErroresPrevistos.detalles(argumento_error))


        print(EstilosImpresionCaracteres.NEGRITA + EstilosImpresionCaracteres.CURSIVA + EstilosImpresionCaracteres.TACHADO + EstilosImpresionCaracteres.INVERTIR_FONDO_CARACTER + 'Mezcado manual')
        print(EstilosImpresionCaracteres.NORMAL + "Sin formato")
        print(EstilosImpresionCaracteres.mix_estilos("NEGRITA", "CURSIVA", "INVERTIR"))


        print(EstilosImpresionCaracteres.NORMAL + "Hola", sep="\n")
        print(ColoresImpresionDisponibles.CARACTER.R + "Hola hola", sep="\n")
        print(ColoresImpresionDisponibles.F0ND0.Y + "Hola hola", sep="\n")
        print(ColoresImpresionDisponibles.CARACTER.C + "Hola hola", sep="\n")
        print(ColoresImpresionDisponibles.F0ND0.M + "Hola hola", sep="\n")
        print(EstilosImpresionCaracteres.NORMAL + "Hola", sep="\n")


