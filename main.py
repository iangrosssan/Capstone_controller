import sys

from PyQt5.QtWidgets import QApplication

from frontend.w_connect import WindowConnect
from frontend.w_calibrate import WindowCalibrate

from backend.routines import timed_back_forth


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


def run():
    routine = window_calibrate.routine
    axis_1 = window_calibrate.axes[0]
    axis_1_type = window_calibrate.axis_setting[axis_1]['axis_type']
    axis_1_position = window_calibrate.axis_setting[axis_1]['position']
    if window_calibrate.axes[1]:
        axis_2 = window_calibrate.axes[1]
        axis_2_type = window_calibrate.axis_setting[axis_2]['axis_type']
        axis_2_position = window_calibrate.axis_setting[axis_2]['position']
    
    if routine == 'Timed Back and Forth' and axis_2 == None:
        timed_back_forth(axis_1, axis_1_type, axis_1_position)
    elif routine == 'Timed Back and Forth' and axis_2 != None:
        timed_back_forth(axis_1, axis_1_type, axis_1_position, axis_2, axis_2_type, axis_2_position)




# INSTANCIAS
window_connect = WindowConnect()
window_calibrate = WindowCalibrate()


# FLUJO
window_connect.show()
window_connect.b_search.clicked.connect(lambda: window_connect.buscar())
window_connect.b_connect.clicked.connect(lambda: window_connect.conectar())
window_connect.b_calibrate.clicked.connect(w_calibrate)
window_calibrate.b_run.clicked.connect(lambda: run())


app.exec_()
