#!/usr/bin/env python3.7

import sys
import logging
from PyQt5 import QtWidgets, QtCore


import gui_module.my_gui_setup
import gui_module.gui as gui


import backend_module.comunication
from backend_module.back_end import ConfigurationData
from copy import deepcopy


def set_logger():
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


def connect_backend(ui,current_configuration_data):
    ui.pushButton_conf_Set_configuration.clicked.connect(lambda: get_vis_configuration_info(ui,current_configuration_data))

def run_window():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = gui_module.gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    gui_module.my_gui_setup.my_setup(ui)

    current_configuration_data = ConfigurationData.create_empty()
    connect_backend(ui,current_configuration_data)

    MainWindow.show()
    app.exec()

def get_vis_configuration_info(ui,current_configuration_data):
    akw_time = ui.spinBox_conf_akw_time.value()
    nr_of_averages = ui.spinBox_conf_averages.value()
    save_loc = ui.lineEdit_conf_data_loc.text()

    save_period_seconds = ui.timeEdit_conf_save_period.time()
    save_period_seconds  = save_period_seconds.minute() * 60 + save_period_seconds.second()
    
    save_type = ui.comboBox_conf_save_type.currentText()
    port_name = ui.comboBox_conf_Port_name.currentText()

    logger.info("Have configuration data")

    new_configuration_data = ConfigurationData(akw_time, nr_of_averages,save_period_seconds, save_loc,save_type,port_name)
    logger.debug(new_configuration_data)
    logger.debug(current_configuration_data)

    current_configuration_data.update_and_drop_diferances(new_configuration_data)
    logger.debug(current_configuration_data)

    set_configuration(current_configuration_data)

def set_configuration(current_configuration_data):
    pass

def get_OneShot_configuration_info(ui):
    file_loc = ui.lineEdit_ss_file_loc.text()
    akw_time = ui.spinBox_ss_akw_time.value()

    return file_loc, akw_time

#simple logging global logger
logger = set_logger()

if __name__ == "__main__":
    run_window()
    logger.info("App closings")
    sys.exit()