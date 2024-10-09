import sys, time

from PyQt5.QtWidgets import QApplication

from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_calibracion import VentanaCalibracion

from backend.funciones import AxisManager, home


# FUNCIONES
def load_stylesheet(filename):
    with open(filename, "r") as file:
        return file.read()

def w_calibrate():
    axis_manager = AxisManager().axes
    ventana_calibracion.axes = axis_manager
    ventana_calibracion.show()    
    ventana_calibracion.setup_ui()


if __name__ == '__main__':
    def hook(type, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    stylesheet = load_stylesheet("frontend/styles.qss")
    app.setStyleSheet(stylesheet)


# INSTANCIAS
ventana_inicio = VentanaInicio()
ventana_calibracion = VentanaCalibracion()


# FLUJO
ventana_inicio.show()
ventana_inicio.b_search.clicked.connect(lambda: ventana_inicio.buscar())
ventana_inicio.b_connect.clicked.connect(lambda: ventana_inicio.conectar())
ventana_inicio.b_calibrate.clicked.connect(w_calibrate)
    
#ventana_inicio.b_calibrate.clicked.connect(lambda: home(ventana_inicio.n_axis_selected))

app.exec_()
