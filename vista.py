import os
import time
from configuracion import *

class Visualizador():

    def __init__(self):
        self.ancho_maximo_caracteres, self.alto_maximo_caracteres = os.get_terminal_size()
        self.limpiar_pantalla()

    def __ajustar_dimensiones(self) -> int:
        pass


    def limpiar_pantalla(self) -> bool:
        # windows
        if os.name == 'nt':
            _ = os.system('cls')
        # Mac and Linux
        else:
            _ = os.system('clear')
        return True

    def pintar_pantalla(self) -> bool:
        if self.limpiar_pantalla():
            pass

    def visualizar_mensaje(self, estado: str = None, mensaje: str = None) -> bool:
        pass

    def visualizar_lista_centros(self, lista_centros: list[dict]) -> bool:
        pass

    def requerir_informacion(self, informacion: dict) -> dict:
        pass

if __name__ == "__main__":
    v = Visualizador()
    v.limpiar_pantalla()