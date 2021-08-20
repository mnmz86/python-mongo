from os import name, system
from configuracion import *

class EstiloPrint():
    HEADER = '\033[95m'
    AZUL = '\033[94m'
    ENCABEZADO_FILA_CYAN = '\033[96m'
    EXITO_VERDE = '\033[92m'
    ADVERTENCIA_AMARILLO = '\033[93m'
    FALLIDO_ROJO = '\033[91m'
    NORMAL_SIN_FORMATO = '\033[0m'
    CON_GROSOR = '\033[1m'
    CON_LINEA = '\033[4m'

class Visualizador():

    def __init__(self):
        pass

    def limpiar_pantalla(self) -> bool:
        # windows
        if name == 'nt':
            _ = system('cls')
        # Mac and Linux
        else:
            _ = system('clear')
        return True

    def pintar_pantalla(self) -> bool:
        if self.limpiar_pantalla():
            pass

    def visualizar_mensaje(self, estado: str = None, mensaje: str = None) -> bool:
        pass

    def visualizar_lista_centros(self, lista_centros: list[dict]) -> bool:
        pass


if __name__ == "__main__":
    v = Visualizador()
    v.limpiar_pantalla()