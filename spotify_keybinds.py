# Runs in the background, sends media commands to Windows when certain keybinds are pressed.
from pynput import keyboard

keyb = keyboard.Controller()

# Which print statements should be displayed?
verbosity = 1

def check_print(statement, verbosity_level=1):
    if verbosity == verbosity_level:
        print(statement)

def press_vk_key(keycode):
    keyb.press(key = keyboard.KeyCode.from_vk(keycode))


# Functions to run when keybinds are pressed
def on_activate_play():
    check_print('Play/Pause activated')
    press_vk_key(179)

def prev_track():
    check_print('Previous Track')
    press_vk_key(177)

def next_track():
    check_print('Next Track')
    press_vk_key(176)
    
def quit():
    check_print("Quitting.")
    exit()

with keyboard.GlobalHotKeys({
        '<alt>+p': on_activate_play,
        '<alt>+j': prev_track,
        '<alt>+k': next_track,
        '<ctrl>+<alt>+q': quit,
        }) as h:
    h.join()