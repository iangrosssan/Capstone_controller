import pathlib, os, time
import matplotlib.pyplot as plt
import libximc.highlevel as ximc
import keyboard, threading


# backend/axis_manager.py
class AxisManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AxisManager, cls).__new__(cls)
            cls._instance.axes = []
        return cls._instance

    def set_axes(self, uris):
        self.axes = [ximc.Axis(uri) for uri in uris]
        print("Axes setted")
        print(self.axes)


# SEÑAL DE TECLADO

def on_key_press(event):
    pass


def keyboard_listener():
    hook = keyboard.on_press(on_key_press)
    keyboard.wait('esc')
    keyboard.unhook(hook)


# CONEXIÓN CON CONTROLADOR
def buscar_devices(): 
    l_devices = []
    devices = ximc.enumerate_devices(
    ximc.EnumerateFlags.ENUMERATE_NETWORK |
    ximc.EnumerateFlags.ENUMERATE_PROBE
    )
    if devices:
        device_uri_1 = devices[0]['uri']
        l_devices.append(device_uri_1)
        device_uri_2 = devices[1]['uri']
        l_devices.append(device_uri_2)

    virtual_device_filename_1 = "virtual_motor_controller_1.bin"
    virtual_device_file_path_1 = os.path.join(
        pathlib.Path().cwd(),
        virtual_device_filename_1
    )

    virtual_device_filename_2 = "virtual_motor_controller_2.bin"
    virtual_device_file_path_2 = os.path.join(
        pathlib.Path().cwd(),
        virtual_device_filename_2
    )
    v_device_uri_1 = "xi-emu:///{}".format(virtual_device_file_path_1)
    l_devices.append(v_device_uri_1)
    v_device_uri_2 = "xi-emu:///{}".format(virtual_device_file_path_2)
    l_devices.append(v_device_uri_2)


    return l_devices, False

    
def conectar_motores(uris):
    manager = AxisManager()
    manager.set_axes(uris)
    return manager.axes

# CONTROL
# A posición cero
def home(axis):
    axis.open_device()
    axis.command_move(0, 0)
    axis.command_wait_for_stop(100)
    print("Axis {} home".format(axis))
    axis.close_device()


def movimiento_axial(axis, pasos, sleep, direccion):
    axis.command_movr(pasos*direccion, 0)
    axis.command_wait_for_stop(sleep)


def movimiento_angular(motor, grados, velocidad, f_l_posicion):
    motor.set_speed(velocidad)
    motor.move_to(grados)
    motor.wait_for_stop()


def parametrizacion(l_axis_1, l_paso, l_sleep, l_axis_2, init, direccion, a_axis=None, a_paso=None, a_sleep=None):
    if any(param is not None for param in [a_axis, a_paso, a_sleep]) and not all(param is not None for param in [a_axis, a_paso, a_sleep]):
        raise ValueError("Si se proporcionan parámetros de movimiento angular, deben ingresarse todos: 'a_axis', 'a_paso' y 'a_sleep'.")
    if not init:
        home(l_axis_1)
        print("Axis_1 in home")
        home(l_axis_2)
        print("Axis_2 in home")
        if a_axis is not None:
            home(a_axis)
        init = True
    
    l_posicion_1 = l_axis_1.get_position().Position
    if l_posicion_1 >= 1000-l_paso and direccion == 1:
        direccion = -1
    elif l_posicion_1 <= 0+l_paso and direccion == -1:
        direccion = 1
    movimiento_axial(l_axis_1, l_paso, l_sleep, direccion)
    print(l_posicion_1)
    l_posicion_2 = l_axis_1.get_position().Position

    if a_axis is not None:
        a_posicion = a_axis.get_position().Position
        f_l_posicion = lambda x: x*l_axis_1.get_position().Position
        movimiento_angular(a_axis, a_paso, a_sleep, f_l_posicion)
    
    if l_posicion_2-l_posicion_1 > 0:
        direccion = 1
    elif l_posicion_2-l_posicion_1 < 0:
        direccion = -1
    return direccion

