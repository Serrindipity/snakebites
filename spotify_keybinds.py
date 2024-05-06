# Runs in the background, sends media commands to Windows when certain keybinds are pressed.
from pynput import keyboard

keyb = keyboard.Controller()

def on_activate_play():
    print('Play/Pause activated')
    keyb.press(key = keyboard.KeyCode.from_vk(179))

def for_canonical(f):
    return lambda k: f(l.canonical(k))

def quit():
    print("Quitting.")
    exit()

with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+p': on_activate_play,
        '<ctrl>+<alt>+q': quit,
        }) as h:
    h.join()