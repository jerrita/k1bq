import serial
import serial.tools.list_ports
import random
import time
import pyautogui
import sys
from termcolor import colored
import configparser
from mouse_driver import MouseMove, ghub_mouse

config = configparser.ConfigParser()
config.read('xxx.ini')

class ArduinoMouse:
    def __init__(self, filter_length=3):
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 115200
        self.serial_port.timeout = 1
        self.serial_port.port = self.find_serial_port()
        self.filter_length = filter_length
        self.x_offset = float(config['Settings']['X_OFFSET'])
        self.y_offset = float(config['Settings']['Y_OFFSET'])

        self.x_history = [0] * filter_length
        self.y_history = [0] * filter_length
        try:
            self.serial_port.open()
        except serial.SerialException:
            print(colored('[Error]', 'red'), colored('The serial port is being used by another application. Close the other application before retrying.', 'white'))
            time.sleep(10)
            sys.exit()

    def find_serial_port(self):
        port = next((port for port in serial.tools.list_ports.comports() if "USB 串行设备" in port.description), None)
        if port is not None:
            return port.device
        else:
            print(colored('[Error]', 'red'), colored('Unable to find serial port or the Arduino device is with different name. Please check its connection and try again.', 'white'))
            time.sleep(10)
            sys.exit()

    def move(self,x, y):
        self.x_history.append(x+self.x_offset)
        self.y_history.append(y+self.y_offset)

        self.x_history.pop(0)
        self.y_history.pop(0)

        smooth_x = int(sum(self.x_history) / self.filter_length)
        smooth_y = int(sum(self.y_history) / self.filter_length)

        finalx = smooth_x + 256 if smooth_x < 0 else smooth_x
        finaly = smooth_y + 256 if smooth_y < 0 else smooth_y
        command = format(finalx, '02x') + format(finaly, '02x')
        self.serial_port.write(b"T" + command.encode('utf-8'))

    def flick(self, x, y):
        x = int(x + 256 if x < 0 else x)
        y = int(y + 256 if y < 0 else y)
        command2 = format(x, '02x') + format(y, '02x')
        self.serial_port.write(b"T" + command2.encode('utf-8'))
        
    def click(self):
        delay = random.uniform(0.01, 0.1)
        self.serial_port.write(b"H")
        time.sleep(delay)
        
    def close(self):
        self.serial_port.close()

    def __del__(self):
        self.close()

class GHubMouse:
    def __init__(self, filter_length=3):
        self.filter_length = filter_length
        self.x_offset = float(config['Settings']['X_OFFSET'])
        self.y_offset = float(config['Settings']['Y_OFFSET'])

        self.x_history = [0] * filter_length
        self.y_history = [0] * filter_length

    def move(self,x, y):
        self.x_history.append(x+self.x_offset)
        self.y_history.append(y+self.y_offset)

        self.x_history.pop(0)
        self.y_history.pop(0)

        smooth_x = int(sum(self.x_history) / self.filter_length)
        smooth_y = int(sum(self.y_history) / self.filter_length)

        # finalx = smooth_x + 256 if smooth_x < 0 else smooth_x
        # finaly = smooth_y + 256 if smooth_y < 0 else smooth_y
        
        MouseMove.ghub_mouse_move(smooth_x, smooth_y)

    def flick(self, x, y):
        # x = int(x + 256 if x < 0 else x)
        # y = int(y + 256 if y < 0 else y)
        MouseMove.ghub_mouse_move(x, y)
        
    def click(self):
        ghub_mouse.mouse_up()
        time.sleep(random.uniform(0.001, 0.003))
        ghub_mouse.mouse_down()
        time.sleep(random.uniform(0.002, 0.005))
        ghub_mouse.mouse_up()
        time.sleep(random.uniform(0.01, 0.05))
        
    def close(self):
        ghub_mouse.mouse_close()

if __name__ == '__main__':
    mouse = GHubMouse()
    # mouse.move(100, 100)
    for i in range(10):
        # mouse.move(100, 100)
        # mouse.move(-100, -100)
        mouse.click()
        time.sleep(0.1)