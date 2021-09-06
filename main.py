from vista import Visualizador
from modelodb import CentroEducativo
import time

class Aplicacion:
    """Enlace entre la vista y la base de datos"""  

    def __init__(self) -> None:
        self.pantalla = Visualizador()
        self.centro_educativo = CentroEducativo()
        self.pantalla.visualizar_mensaje(self.centro_educativo.estado_conexion)
        time.sleep(1)
        self.pantalla.limpiar_pantalla()
        self.inicializa_aplicacion()



    def inicializa_aplicacion(self):
        pass
if __name__=="__main__":
    Aplicacion()