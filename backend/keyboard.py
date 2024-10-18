import keyboard, threading

# SEÑAL DE TECLADO
def on_key_press(event):
    pass


def keyboard_listener():
    hook = keyboard.on_press(on_key_press)
    keyboard.wait('esc')
    keyboard.unhook(hook)

listener = threading.Thread(target=keyboard_listener)
