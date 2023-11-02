import time

import serial
from serial.serialutil import SerialException
import yaml
import win32gui, win32process, psutil
from threading import Thread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtCore import *

class DygmaDefyController:
    def __init__(self):
        self.load_config()
        self.last_layer = "-1"
        self.last_brightness = -1
        # auto switcher thread
        Thread(target=self.auto_switcher, daemon=True).start()

        self.tray_menu()

    def auto_switcher(self):
        time.sleep(2)
        while True:
            self.load_config()

            # layer control
            current_window = self.get_current_window()
            if current_window != self.config["bazecor"]:
                layer = self.match_window(current_window)
                if self.last_layer != layer:
                    self.switch_layer(layer)
                    self.last_layer = layer
                time.sleep(self.config["refresh_interval"])
    def switch_layer(self, layer: int | str):
        try:
            layer_switch_command = f"layer.moveTo {layer}".encode()
            if self.config["mode"] == "rf" \
                    or self.config["mode"] == "wired":
                # send command via serial communication
                ser = serial.Serial(self.config['PORT'])
                ser.write(layer_switch_command)
                ser.close()
            elif self.config["mode"] == "bluetooth" \
                or self.config["mode"] == "bl":
                # send command via bluetooth
                pass
            print(f"Switched to layer {layer}")
        except AttributeError as err:
            print(f"An Error occurred communicating with the keyboard on port {self.config['PORT']}\nRetrying in 15 s")
            # time.sleep(15)
        except SerialException as err:
            print(f"Could not open seriel port {self.config['PORT']}, make sure the keyboard is connected and the port matches.")

    def match_window(self, process_name: str):
        '''
        matches, if the current window is in the layer change list
        :param window_name:
        :return:
        '''
        try:
            for layer in self.config["layers"]:
                if any(program.lower() in process_name.lower() for program in self.config["layers"][layer]):
                    return layer
            else:
                return self.config["base_layer"]
        except AttributeError:
            print("Failed gettings process name, returning last layer")
            return self.last_layer

    def get_current_window(self):
        '''
        returns the name of the current window
        :return:
        '''
        try:
            pid = win32process.GetWindowThreadProcessId(win32gui.GetForegroundWindow())
            return (psutil.Process(pid[-1]).name())
        except:
            pass

    def load_config(self):
        while True:
            try:
                with open('config.yaml', 'r') as cf:
                    self.config = yaml.load(cf, yaml.Loader)

            except:
                pass
            else:
                break

    def _quit(self):
        exit(0)

    def tray_menu(self):
        self.app = QApplication([])
        self.icon = QIcon("icons/dygma.ico")
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)
        self.app.setQuitOnLastWindowClosed(False)

        # Tray-Menu
        menu = QMenu()

        menu.addSeparator()

        option_close = QAction("Close")
        option_close.triggered.connect(self._quit)
        menu.addAction(option_close)

        self.tray.setContextMenu(menu)
        self.app.exec_()


if __name__ == "__main__":
    app = DygmaDefyController()
