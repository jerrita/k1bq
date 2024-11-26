import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime
import configparser
import keyboard
import pyautogui
from termcolor import colored
from colorant import Colorant
import random
import ctypes
import string


config = configparser.ConfigParser()
config.read('xxx.ini')

TOGGLE_KEY = config['Settings']['TOGGLE_KEY']
XFOV = int(config['Settings']['XFOV'])
YFOV = int(config['Settings']['YFOV'])
INGAME_SENSITIVITY = float(config['Settings']['INGAME_SENSITIVITY'])
FLICKSPEED = 1.07437623 * (INGAME_SENSITIVITY ** -0.9936827126)
MOVESPEED = float(config['Settings']['SMOOTH']) / (5 * INGAME_SENSITIVITY)

monitor = pyautogui.size()
CENTER_X, CENTER_Y = monitor.width // 2, monitor.height // 2

def generate_random_title(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def set_window_title_random():
    random_title = generate_random_title()
    os.system('title ' + random_title)
    return random_title

def ensure_admin():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
        exit(-1)

def hide_proc():
    from ctypes import CDLL
    import os
    try:
        hph = CDLL(os.path.join(os.path.dirname(__file__), 'HideProcessHook.dll'))
    except Exception as e:
        print('Failed to load HideProcessHook.dll:', e)


def main():
    random_title = set_window_title_random()
    ensure_admin()
    hide_proc()
    colorant = Colorant(CENTER_X - XFOV // 2, CENTER_Y - YFOV // 2, XFOV, YFOV, FLICKSPEED, MOVESPEED)

    print()
    status = 'Disabled'
    
    try:
        while True:
            if keyboard.is_pressed(TOGGLE_KEY):
                colorant.toggle()
                status = 'Enabled ' if colorant.toggled else 'Disabled'
            print(f'\r{colored("[Status]", "green")} {colored(status, "white")}', end='')
            time.sleep(0.01)
    except (KeyboardInterrupt, SystemExit):
        print(colored('\n[Info]', 'green'), colored('Exiting...', 'white') + '\n')
    finally:
        colorant.close()

if __name__ == '__main__':
    main()

 

