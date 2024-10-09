import sys

from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QHeaderView
from PyQt5.QtGui import QFont
from PyQt5.uic import loadUiType

from backend.funciones import buscar_devices, conectar_motores

window_name, base_class = loadUiType("frontend/ventana_inicio.ui")


class VentanaInicio(window_name, base_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.n_axis_selected = 0
        self.b_connect.setEnabled(False)
        self.b_calibrate.setEnabled(False)
        self.b_run.setEnabled(False)
        self.t_device.horizontalHeader().setFixedHeight(40)
        self.t_device.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)       
        self.t_device.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
    
    def buscar(self):
        device = buscar_devices()
        self.t_device.setRowCount(len(device[0]))
        for i in range(len(device[0])):
            self.t_device.setItem(i,0,QTableWidgetItem(device[0][i]))
            if not device[1]:
                self.t_device.setItem(i,1,QTableWidgetItem("Virtual"))
            else:
                self.t_device.setItem(i,1,QTableWidgetItem("Real"))
        self.activar_conectar()
    
    def conectar(self):
        devices = self.t_device.selectedItems()
        uris = []
        for i in devices:
            if i.column() == 0:
                uris.append(i.text())
        self.n_axis_selected = len(uris)
        conectar_motores(uris)
        self.activar_calibrar()
        self.activar_ejecutar()

    def activar_conectar(self):
        self.b_connect.setEnabled(True)

    def activar_calibrar(self):
        self.b_calibrate.setEnabled(True)    

    def activar_ejecutar(self):
        self.b_run.setEnabled(True)



if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaInicio()
    ventana.show()
    sys.exit(app.exec_())
