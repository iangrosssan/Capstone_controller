import sys

from PyQt5.QtWidgets import QApplication, QGridLayout, QVBoxLayout, QPushButton, QLabel, QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUiType

from backend.funciones import home

window_name, base_class = loadUiType("frontend/ventana_calibracion.ui")


class VentanaCalibracion(window_name, base_class):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.axes = []
        self.home_buttons = []
        self.set_range_buttons = []
        self.fix_buttons = []

    def setup_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Grid layout for buttons
        grid_layout = QGridLayout()

        for i in range(len(self.axes)):
            axis_label = QLabel(f"Axis {i + 1}")
            axis_label.setObjectName("regular")
            grid_layout.addWidget(axis_label, i, 0, alignment=Qt.AlignCenter)

            home_button = QPushButton("Home")
            home_button.setObjectName(f"b_home_{i + 1}")  # Unique object name
            self.home_buttons.append(home_button)
            home_button.setCursor(Qt.PointingHandCursor)
            home_button.clicked.connect(lambda _, ax=self.axes[i]: home(ax))
        
            set_range_button = QPushButton("Set range")
            set_range_button.setObjectName(f"b_set_range_{i + 1}")  # Unique object name
            self.set_range_buttons.append(set_range_button)
            set_range_button.setCursor(Qt.PointingHandCursor)
        
            fix_button = QPushButton("Fix")
            fix_button.setObjectName(f"b_fix_{i + 1}")  # Unique object name
            self.fix_buttons.append(fix_button)
            fix_button.setCursor(Qt.PointingHandCursor)

            grid_layout.addWidget(home_button, i, 1)
            grid_layout.addWidget(set_range_button, i, 2)
            grid_layout.addWidget(fix_button, i, 3)

        main_layout.addStretch()
        main_layout.addLayout(grid_layout)
        main_layout.addStretch()

if __name__ == '__main__':
    app = QApplication([])
    ventana = VentanaCalibracion()
    ventana.show()
    sys.exit(app.exec_())
