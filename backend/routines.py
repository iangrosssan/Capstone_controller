import time
import keyboard, threading

from backend.keyboard import keyboard_listener


# CONTROL
# A posición cero
def home(axis_number, axis, position_changed_signal):
    axis.open_device()
    axis.command_move(0, 0)
    axis.command_wait_for_stop(100)
    position_changed_signal.emit(axis_number, 0, axis.get_position().Position)
    axis.close_device()
    

def tare(axis_number, axis, position_changed_signal):
    axis.open_device()
    axis.command_zero()
    position_changed_signal.emit(axis_number, 0, axis.get_position().Position)
    axis.close_device()


def set_range(axis_number, axis, position_changed_signal):
    axis.open_device()
    lower_range = joystick(axis_number, axis, 2, position_changed_signal)
    time.sleep(0.5)
    upper_range = joystick(axis_number, axis, 3, position_changed_signal)
    axis.close_device()
    return lower_range, upper_range


def fix(axis_number, axis, position_changed_signal):
    axis.open_device()
    fixed_position = joystick(axis_number, axis, 1, position_changed_signal)
    axis.close_device()
    return fixed_position


def joystick(axis_number, axis, position_type, position_changed_signal):
    listener = threading.Thread(target=keyboard_listener)
    listener.start()

    while listener.is_alive():
        if keyboard.is_pressed('right'):
            axis.command_movr(20, 0)
            axis.command_wait_for_stop(100)
            position_changed_signal.emit(axis_number, position_type, axis.get_position().Position)
        if keyboard.is_pressed('left'):
            axis.command_movr(-20, 0)
            axis.command_wait_for_stop(100)
            position_changed_signal.emit(axis_number, position_type, axis.get_position().Position)
        if keyboard.is_pressed('enter'):
            print('enter')
            return axis.get_position().Position


def run_back_forth(range_axis, range, fixed_axis=None, fixed_position=None):
    pass

    
def movimiento_axial(axis, pasos, sleep, direccion):
    axis.command_movr(pasos*direccion, 0)
    axis.command_wait_for_stop(sleep)


def parametrizacion(l_axis_1, l_paso, l_sleep, l_axis_2, init, direccion):
    if not init:
        home(l_axis_1)
        print("Axis_1 in home")
        home(l_axis_2)
        print("Axis_2 in home")
        init = True
    
    l_posicion_1 = l_axis_1.get_position().Position
    if l_posicion_1 >= 1000-l_paso and direccion == 1:
        direccion = -1
    elif l_posicion_1 <= 0+l_paso and direccion == -1:
        direccion = 1
    movimiento_axial(l_axis_1, l_paso, l_sleep, direccion)
    print(l_posicion_1)
    l_posicion_2 = l_axis_1.get_position().Position
    
    if l_posicion_2-l_posicion_1 > 0:
        direccion = 1
    elif l_posicion_2-l_posicion_1 < 0:
        direccion = -1
    return direccion

