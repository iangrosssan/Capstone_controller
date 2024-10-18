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


def timed_back_forth(axis_1, axis_type_1, position_1, axis_2=None, axis_type_2=None, position_2=None, step=20):
    if axis_type_1 == 'range':
        axis_1.open_device()
        axis_1.command_move(position_1[0], 0)
        axis_1.command_wait_for_stop(100)
        pos = position_1[0]
        while True:
            while pos <= position_1[1] - step:
                axis_1.command_move(pos, 0)
                axis_1.command_wait_for_stop(100)
                pos += step
                print("Current position:", axis_1.get_position().Position)

            # Move axis_1 to position 0 with step 300
            while pos >= position_1[0] + step:
                axis_1.command_move(pos, 0)
                axis_1.command_wait_for_stop(100)
                pos -= step
                print("Current position:", axis_1.get_position().Position)
        axis_1.close_device()
    if axis_type_2 == 'range':
        axis_2.open_device()
        axis_2.command_move(position_2[0], 0)
        axis_2.command_wait_for_stop(100)
        pos = position_2[0]
        while True:
            while pos <= position_2[1] - step:
                axis_2.command_move(pos, 0)
                axis_2.command_wait_for_stop(100)
                pos += step
                print("Current position:", axis_2.get_position().Position)

            # Move axis_1 to position 0 with step 300
            while pos >= position_2[0] + step:
                axis_2.command_move(pos, 0)
                axis_2.command_wait_for_stop(100)
                pos -= step
                print("Current position:", axis_2.get_position().Position)
        axis_2.close_device()
    

    
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

