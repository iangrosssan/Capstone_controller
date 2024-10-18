from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.uic import loadUiType

from backend.routines import home, tare, set_range, fix

window_name, base_class = loadUiType("frontend/w_calibrate.ui")


class WindowCalibrate(window_name, base_class):
    position_changed = pyqtSignal(int, int, float)
    axis_ready = pyqtSignal(int, int, float)

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        
        self.axes = []
        self.routine = None
        self.axis_setting = {}

        self.axis_labels = []
        self.home_buttons = []
        self.set_home_buttons = []
        self.set_range_buttons = []
        self.fix_buttons = []

        #self.b_run.setEnabled(False)

        self.position_changed.connect(self.update_axis_label)
        self.axis_ready.connect(self.set_axis)


    def setup_ui(self):
        self.l_title.setText(self.routine)

        for i, axis in enumerate(self.axes):
            axis.open_device()
            axis_label = QLabel(f"Axis {i + 1}\n{axis.get_position().Position}\n")
            axis.close_device()
            axis_label.setObjectName("regular")
            self.axis_labels.append(axis_label)
            self.gridLayout.addWidget(axis_label, i, 0, alignment=Qt.AlignCenter)


        for i in range(len(self.axes)):
            home_button = QPushButton("Home")
            home_button.setObjectName(f"b_home_{i+1}")  # Unique object name
            self.home_buttons.append(home_button)
            home_button.setCursor(Qt.PointingHandCursor)
            home_button.clicked.connect(lambda _, ax_n=i, ax=self.axes[i]: home(ax_n, ax, self.position_changed))
        
            tare_button = QPushButton("Tare")
            tare_button.setObjectName(f"b_tare_{i+1}")
            self.set_home_buttons.append(tare_button)
            tare_button.setCursor(Qt.PointingHandCursor)
            tare_button.clicked.connect(lambda _, ax_n=i, ax=self.axes[i]: tare(ax_n, ax, self.position_changed))

            set_range_button = QPushButton("Set Range")
            set_range_button.setObjectName(f"b_set_range_{i+1}")  # Unique object name
            self.set_range_buttons.append(set_range_button)
            set_range_button.setCursor(Qt.PointingHandCursor)
            set_range_button.clicked.connect(lambda _, ax_n=i, ax=self.axes[i]: set_range(ax_n, ax, self.position_changed))
        
            fix_button = QPushButton("Fix")
            fix_button.setObjectName(f"b_fix_{i+1}")  # Unique object name
            self.fix_buttons.append(fix_button)
            fix_button.setCursor(Qt.PointingHandCursor)
            fix_button.clicked.connect(lambda _, ax_n=i, ax=self.axes[i]: fix(ax_n, ax, self.position_changed))

            self.gridLayout.addWidget(home_button, i, 1)
            self.gridLayout.addWidget(tare_button, i, 2)
            self.gridLayout.addWidget(set_range_button, i, 3)
            self.gridLayout.addWidget(fix_button, i, 4)
    

    def update_axis_label(self, axis_number, position_type, position):
        if position_type == 0:
            self.axis_labels[axis_number].setText(f"Axis {axis_number+1}\n{int(position)}\n")
            self.axis_labels[axis_number].repaint()

        elif position_type == 1:
            self.axis_labels[axis_number].setText(f"Axis {axis_number+1}\nFix: {int(position)}\n")
            self.axis_labels[axis_number].adjustSize()
            self.axis_labels[axis_number].repaint()
            self.axis_setting[self.axes[axis_number]] = {'axis_type': 'fix', 'position': [int(position)]}

        elif position_type == 2:
            self.axis_labels[axis_number].setText(f"Axis {axis_number+1}<br>Lower: {int(position)}<br>Upper: -")
            self.axis_labels[axis_number].adjustSize()
            self.axis_labels[axis_number].repaint()
            self.axis_setting[self.axes[axis_number]] = {'axis_type': 'range', 'position': [int(position)]}

        elif position_type == 3:
            low_bound = int(self.axis_setting[self.axes[axis_number]]['position'][0])
            self.axis_labels[axis_number].setText(f"Axis {axis_number+1}<br>Lower: {low_bound}<br>Upper: {int(position)}")
            self.axis_labels[axis_number].adjustSize()
            self.axis_labels[axis_number].repaint()
            if len(self.axis_setting[self.axes[axis_number]]['position']) > 1:
                self.axis_setting[self.axes[axis_number]]['position'][1] = int(position)
            else:
                self.axis_setting[self.axes[axis_number]]['position'].append(int(position))
        

    def set_axis(self, axis_number, position):
        if axis_number == 0:
            self.axis_1_position = position
            self.axis_1_state = True
        elif axis_number == 1:
            self.axis_2_position = position
            self.axis_2_state = True
        
        if self.axis_1_state and self.axis_2_state:
            self.b_run.setEnabled(True)
            self.b_run.clicked.connect(self.run_routine)