#!/usr/bin/env python3.7

import sys
import logging
from PyQt5 import QtWidgets


import gui_module.my_gui_setup
import gui_module.gui as gui


import backend_module.comunication

def set_logger():
    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%I:%M:%S %p')
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',datefmt="%H:%M:%S")
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.debug("Created logger")

    return logger


#simple logging global logger
logger = set_logger()

def connect_backend(ui):
    ui.pushButton_conf_Set_configuration.clicked.connect(lambda: get_vis_configuration_info(ui))

def run_window():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = gui_module.gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    gui_module.my_gui_setup.my_setup(ui)

    connect_backend(ui)

    MainWindow.show()
    app.exec()

def get_vis_configuration_info(ui):
    akw_time = ui.spinBox_conf_akw_time.value()
    print(akw_time)

if __name__ == "__main__":
    run_window()
    logger.info("App closings")
    sys.exit()