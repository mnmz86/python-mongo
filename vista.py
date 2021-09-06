import os
from typing import Union,Optional
from configuracion import (
    UbicacionCentroEscolar as Ubicacion,
    AtributosCentroEscolar as CE,
    ColoresImpresionDisponibles as Color,
    EstilosImpresionCaracteres as Estilo,
    Respuestas as Resp,
    con_gestion_de_errores
)
class Visualizador():

    def __init__(self):
        self.ancho_maximo_caracteres, self.alto_maximo_caracteres = os.get_terminal_size()
        self.ancho_codigo_infraestructura = 5
        self.ancho_departamento = 12
        self.ancho_municipio = 25
        self.ancho_centro_escolar = self.ancho_maximo_caracteres - (
            12 # 4 caracteres extra por los tres campos
            + self.ancho_codigo_infraestructura
            + self.ancho_departamento
            + self.ancho_municipio
            )
        self.limpiar_pantalla()


    def limpiar_pantalla(self) -> None:
        # windows
        if os.name == 'nt':
            _ = os.system('cls')
        # Mac and Linux
        else:
            _ = os.system('clear')

    def pintar_pantalla(self) -> bool:
        estilo_cabecera = Estilo.NEGRITA+ Color.F0ND0.D + Color.CARACTER.M
        linea_decorativa = "*"*self.ancho_maximo_caracteres
        aplicacion_saludo = f"""*{"CONTROL DE LISTADO DE CENTROS ESCOLARES".center(self.ancho_maximo_caracteres - 2)}*
        \r*{"¡Bienvenido!".center(self.ancho_maximo_caracteres - 2)}*"""
        cabecera = \
            f"""{estilo_cabecera + linea_decorativa}
            \r{aplicacion_saludo}
            \r{linea_decorativa + Estilo.NORMAL}
            """
        print(cabecera)
        
        return True

    def visualizar_mensaje(self, data: dict[str, str], espera_respuesta: Optional[bool]) -> bool:
        mensaje = ""
        if data[Resp.ESTADO]==Resp.FALLIDO:
            mensaje = \
            f"""{Estilo.NEGRITA + Color.F0ND0.Y + Color.CARACTER.D + "ERROR:".center(self.ancho_maximo_caracteres)}
            \r{Estilo.NORMAL + Color.F0ND0.D + Color.CARACTER.R + data[Resp.CONTENIDO].ljust(self.ancho_maximo_caracteres)}
            {Estilo.NORMAL}"""
        else:
            mensaje = \
            f"""{Estilo.NEGRITA + Color.F0ND0.B + "INFORMACIÓN:".center(self.ancho_maximo_caracteres)}
            \r{Estilo.NORMAL + Color.F0ND0.D + Color.CARACTER.G + data[Resp.CONTENIDO].center(self.ancho_maximo_caracteres)}
            {Estilo.NORMAL}"""
        print(mensaje)
        return input("\n>") if espera_respuesta else None

    def visualizar_lista_centros(self, lista_centros: list[dict[str,Union[str, int]]]) -> bool:
        contenido_filas = ""
        for indice_fila, centro_escolar in enumerate(lista_centros):
            codigo, nombre, departamento, municipio = self.formatear_fila_centro_escolar(centro_escolar)
            fondo = None
            if indice_fila%2:
                fondo = Color.F0ND0.B
            else:
                fondo = Color.F0ND0.D
            contenido_filas += (
                fondo
                + Color.CARACTER.W
                + f"  {codigo} | {nombre} | {departamento} | {municipio} \n{Estilo.NORMAL}"
            )
        print(contenido_filas)
        return True


    def formatear_fila_centro_escolar(self, centro) -> tuple:
            codigo = str(centro[CE.CODIGO]).center(self.ancho_codigo_infraestructura, " ")
            nombre = centro[CE.NOMBRE].center(self.ancho_centro_escolar, " ")
            departamento = centro[CE.DEPARTAMENTO_CENTRO].center(self.ancho_departamento, " ")
            municipio = centro[CE.MUNICIPIO_CENTRO] .center(self.ancho_municipio, " ")
            return codigo, nombre, departamento, municipio


    def seleccionar_municipio(self, departamento: int):
        municipios = Ubicacion
        ancho_maximo =  self.ancho_municipio
        mensaje = "Por favor escriba el número correspondiente al Municipio"


    def seleccionar_ubicacion(self, mensaje: str, diccionario_ubicaciones: dict) -> bool:
        opciones_ubicacion = None
        print(opciones_ubicacion)
        diccionario_mensaje = Resp.preparar_respuesta(Resp.EXITOSO, Resp.MENSAJE, mensaje)
        numero_ubicacion = self.visualizar_mensaje(diccionario_mensaje, True)
        return numero_ubicacion

if __name__ == "__main__":
    v = Visualizador()
    v.limpiar_pantalla()
    v.pintar_pantalla()