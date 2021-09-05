import os
from typing import Union
from configuracion import *
from configuracion import (
    AtributosCentroEscolar as CE,
    ColoresImpresionDisponibles as Color,
    EstilosImpresionCaracteres as Estilo
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


    def limpiar_pantalla(self) -> bool:
        # windows
        if os.name == 'nt':
            _ = os.system('cls')
        # Mac and Linux
        else:
            _ = os.system('clear')
        return True

    def pintar_pantalla(self) -> bool:
            pass

    def visualizar_mensaje(self, data: dict[str, str]) -> bool:
        mensaje = ""
        if data[Respuestas.ESTADO]==Respuestas.FALLIDO:
            mensaje = \
            f"""{Estilo.NEGRITA + Color.F0ND0.Y + Color.CARACTER.D + "ERROR:".center(self.ancho_maximo_caracteres)}
            \r{Estilo.NORMAL + Color.F0ND0.D + Color.CARACTER.R + data[Respuestas.CONTENIDO].ljust(self.ancho_maximo_caracteres)}
            {Estilo.NORMAL}"""
        else:
            mensaje = \
            f"""{Estilo.NEGRITA + Color.F0ND0.B + "INFORMACIÓN:".center(self.ancho_maximo_caracteres)}
            \r{Estilo.NORMAL + Color.F0ND0.D + Color.CARACTER.G + data[Respuestas.CONTENIDO].center(self.ancho_maximo_caracteres)}
            {Estilo.NORMAL}"""
        print(mensaje)
        return True

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

    def requerir_informacion(self, informacion: dict) -> dict:
        pass

    def formatear_fila_centro_escolar(self, centro):
            codigo = str(centro[CE.CODIGO]).center(self.ancho_codigo_infraestructura, " ")
            nombre = centro[CE.NOMBRE].center(self.ancho_centro_escolar, " ")
            departamento = centro[CE.DEPARTAMENTO_CENTRO].center(self.ancho_departamento, " ")
            municipio = centro[CE.MUNICIPIO_CENTRO] .center(self.ancho_municipio, " ")
            return codigo, nombre, departamento, municipio


if __name__ == "__main__":
    v = Visualizador()
    v.limpiar_pantalla()
    print(v.ancho_centro_escolar)