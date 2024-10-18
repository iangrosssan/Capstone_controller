import sys

from PyQt5.QtWidgets import QApplication

from frontend.w_connect import WindowConnect
from frontend.w_calibrate import WindowCalibrate

if __name__ == '__main__':
    def hook(type, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    with open("frontend/styles.qss", "r") as file:
        stylesheet = file.read()
        app.setStyleSheet(stylesheet)


def w_calibrate():
    window_calibrate.axes = window_connect.axes
    window_calibrate.routine = window_connect.routine
    window_calibrate.show()    
    window_calibrate.setup_ui()


# INSTANCIAS
window_connect = WindowConnect()
window_calibrate = WindowCalibrate()


# FLUJO
window_connect.show()
window_connect.b_search.clicked.connect(lambda: window_connect.buscar())
window_connect.b_connect.clicked.connect(lambda: window_connect.conectar())
window_connect.b_calibrate.clicked.connect(w_calibrate)


app.exec_()
