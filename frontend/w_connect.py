from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt

from backend.funciones import buscar_devices, conectar_motores

window_name, base_class = loadUiType("frontend/w_connect.ui")


class WindowConnect(window_name, base_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.axes = []
        self.routine = None
        self.b_connect.setEnabled(False)
        self.b_calibrate.setEnabled(False)
        self.t_device.horizontalHeader().setFixedHeight(45)
        self.t_routines.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.t_device.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.t_device.horizontalHeaderItem(1).setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.t_device.itemSelectionChanged.connect(self.activate_connect)
        self.t_device.itemSelectionChanged.connect(self.activate_calibrate)
        self.t_routines.itemSelectionChanged.connect(self.activate_calibrate)
        

    def buscar(self):
        device = buscar_devices()
        self.t_device.setRowCount(len(device))
        for i in range(len(device)):
            self.t_device.setItem(i,0,QTableWidgetItem(device[i][0]))
            self.t_device.setItem(i,1,QTableWidgetItem(device[i][1]))


    def conectar(self):
        devices = self.t_device.selectedItems()
        uris = []
        for i in devices:
            if i.column() == 0:
                uris.append(i.text())
        self.axes = conectar_motores(uris)


    def activate_connect(self):
        if self.t_device.selectedItems():
            self.b_connect.setEnabled(True)

    def activate_calibrate(self):
        if self.t_routines.selectedItems() and self.t_device.selectedItems():
            self.b_calibrate.setEnabled(True)
