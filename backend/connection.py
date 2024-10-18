import os, pathlib

from backend.classes import AxisManager


# CONEXIÓN CON CONTROLADOR
def buscar_devices(): 
    l_devices = []
    # devices = ximc.enumerate_devices(
    # ximc.EnumerateFlags.ENUMERATE_NETWORK |
    # ximc.EnumerateFlags.ENUMERATE_PROBE
    # )
    # if devices:
    #     device_uri_1 = devices[0]['uri']
    #     l_devices.append([device_uri_1, "Real"])
    #     device_uri_2 = devices[1]['uri']
    #     l_devices.append([device_uri_2, "Real"])

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
    l_devices.append([v_device_uri_1, "Virtual"])
    v_device_uri_2 = "xi-emu:///{}".format(virtual_device_file_path_2)
    l_devices.append([v_device_uri_2, "Virtual"])

    return l_devices

    
def conectar_motores(uris):
    manager = AxisManager()
    manager.set_axes(uris)
    return manager.axes
