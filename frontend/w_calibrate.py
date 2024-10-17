from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.uic import loadUiType

from backend.funciones import home, set_range, fix

window_name, base_class = loadUiType("frontend/w_calibrate.ui")


class WindowCalibrate(window_name, base_class):
    position_changed = pyqtSignal(int,float)

    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.axes = []
        self.home_buttons = []
        self.set_range_buttons = []
        self.fix_buttons = []

        self.position_changed.connect(self.update_axis_label)


    def setup_ui(self):
        self.l_title.setText(self.routine)
        if len(self.axes) >= 1:
            self.axes[0].open_device()
            self.axis_label_1 = QLabel(f"Axis {1}\n{self.axes[0].get_position().Position}")
            self.axes[0].close_device()
            self.axis_label_1.setObjectName("regular")
            self.gridLayout.addWidget(self.axis_label_1, 0, 0, alignment=Qt.AlignCenter)
        if len(self.axes) == 2:
            self.axes[1].open_device()
            self.axis_label_2 = QLabel(f"Axis {2}\n{self.axes[1].get_position().Position}")
            self.axes[1].close_device()
            self.axis_label_2.setObjectName("regular")
            self.gridLayout.addWidget(self.axis_label_2, 1, 0, alignment=Qt.AlignCenter)

        for i in range(len(self.axes)):
            home_button = QPushButton("Home")
            home_button.setObjectName(f"b_home_1")  # Unique object name
            self.home_buttons.append(home_button)
            home_button.setCursor(Qt.PointingHandCursor)
            home_button.clicked.connect(lambda _, ax_n=i, ax=self.axes[i]: home(ax_n, ax, self.position_changed))
        
            set_range_button = QPushButton("Set range")
            set_range_button.setObjectName(f"b_set_range_{i + 1}")  # Unique object name
            self.set_range_buttons.append(set_range_button)
            set_range_button.setCursor(Qt.PointingHandCursor)
            set_range_button.clicked.connect(lambda _, ax_n=i, ax=self.axes[i]: set_range(ax_n, ax, self.position_changed))
        
            fix_button = QPushButton("Fix")
            fix_button.setObjectName(f"b_fix_{i + 1}")  # Unique object name
            self.fix_buttons.append(fix_button)
            fix_button.setCursor(Qt.PointingHandCursor)
            fix_button.clicked.connect(lambda _, ax_n=1, ax=self.axes[i]: fix(ax_n, ax, self.position_changed))

            self.gridLayout.addWidget(home_button, i, 1)
            self.gridLayout.addWidget(set_range_button, i, 2)
            self.gridLayout.addWidget(fix_button, i, 3)
    

    def update_axis_label(self, axis_number, position):
        if axis_number == 0:
            print("Updating axis label1", position)
            self.axis_label_1.setText(f"Axis {1}\n{int(position)}")
            self.axis_label_1.repaint()
        elif axis_number == 1:
            print("Updating axis label2", position)
            self.axis_label_2.setText(f"Axis {2}\n{int(position)}")
            self.axis_label_1.repaint()
