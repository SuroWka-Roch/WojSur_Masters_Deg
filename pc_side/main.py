#!/usr/bin/env python3.7

import sys
import logging
from PyQt5 import QtWidgets, QtCore

from serial import SerialException
from serial import Serial

import time
import threading


import gui_module.my_gui_setup
import gui_module.gui as gui


import backend_module.comunication
from backend_module.back_end import ConfigurationData
from copy import deepcopy

from backend_module.back_end import CountRateData, rawLogClass,back_end_deamon
from backend_module.back_end import ExpectedResponseNotFound, NoReadyToResponse, CommunicationError
from backend_module.configuration import REPEAT_FOR


def set_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt="%H:%M:%S")
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
    logger.debug("Created logger")

    return logger


def configure_arduino(serial_port, current_configuration_data, log, silence = False):
    return comunication_function_hendler_funtion(lambda: backend_module.comunication.configure_all(
            serial_port, current_configuration_data, log), silence= silence)
        



def popup_window(msg):
    error_dialog = QtWidgets.QErrorMessage()
    error_dialog.showMessage(msg)
    error_dialog.exec_()

def comunication_function_hendler_funtion(fun,silence = False):
    try:
        fun()
    except SerialException as e:
        if not silence:
            popup_window(
                'Bad port - could not open port with given name "{}". \n Message error of "{}"'.format(port_name, str(e)))
        return False
    except CommunicationError as e:
        if not silence:
            popup_window(
                'Bad response from arduino. Make sure right program is running on controler.')
        return False

    except Exception as e:
        if not silence:
            popup_window('exeption with message of {}'.format(str(e)))
        return False
    else:
        return True

def try_port(SerialPort, current_configuration_data, silence = False):
    port_name = current_configuration_data.data["port_name"]
    return comunication_function_hendler_funtion(lambda: backend_module.comunication.try_port(port_name, SerialPort), silence= silence)

def configuration_buttom_func(ui, current_configuration_data, serial_port, log, semaphore):
    get_vis_configuration_info(ui, current_configuration_data)
    logger.debug(current_configuration_data)
    logger.debug(serial_port)
    if current_configuration_data["port_name"] == "Not connected":
        popup_window("Pick a port")
        return
    with semaphore:
        for tries in range(REPEAT_FOR):
            if try_port(serial_port, current_configuration_data, silence=True if  not tries == REPEAT_FOR -1 else False ):
                break
        else:
            return
        for tries in range(REPEAT_FOR):
            if configure_arduino(serial_port, current_configuration_data, log, silence=True if  not tries == REPEAT_FOR -1 else False ):
                break
    logger.info("Have connection to serial port:\n{}\nWith setting of:\n{}".format(serial_port,current_configuration_data))



def connect_backend(ui, current_configuration_data, serial_port, log, semaphore):
    ui.pushButton_conf_Set_configuration.clicked.connect(
        lambda: configuration_buttom_func(ui, current_configuration_data, serial_port, log, semaphore))
    ui.pushButton_conf_start.clicked.connect(
        lambda: start_buttom_function(semaphore, serial_port, log)
    )
    ui.pushButton_conf_stop.clicked.connect(lambda: stop_buttom_function(semaphore,serial_port,log))

def start_buttom_function(semaphore,serial_port,log):
    with semaphore:
        for tries in range(REPEAT_FOR):
            if comunication_function_hendler_funtion(lambda: backend_module.comunication.start(serial_port,log), silence=True if  not tries == REPEAT_FOR -1 else False):
                break

def stop_buttom_function(semaphore,serial_port,log):
    with semaphore:
        for tries in range(REPEAT_FOR):
            if comunication_function_hendler_funtion(lambda: backend_module.comunication.stop(serial_port,log), silence=True if  not tries == REPEAT_FOR -1 else False):
                break
def run_window():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = gui_module.gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    gui_module.my_gui_setup.my_setup(ui)

    #Value holders
    serial_port = Serial()
    current_configuration_data = ConfigurationData.create_empty()
    log = rawLogClass()
    data = CountRateData(gui_module.configuration.CANAL_NAMES,ui.spinBox_conf_akw_time.value)
    serial_port_semaphore = threading.Semaphore()
    thread = create_backend_deamon(data, serial_port_semaphore , log, serial_port)
    thread.start()

    #timers
    timer = QtCore.QTimer()
    timer.timeout.connect(lambda : print(log.return_chunk()))
    timer.start(5000)

    connect_backend(ui, current_configuration_data, serial_port, log, serial_port_semaphore)

    MainWindow.show()
    app.exec()

    

def create_backend_deamon(count_rate_data, semaphore, log, serial_port):
    thread = threading.Thread(target=back_end_deamon, args=(count_rate_data, semaphore, log, serial_port), daemon=True, name="reading data")
    return thread

def get_vis_configuration_info(ui, current_configuration_data):
    akw_time = ui.spinBox_conf_akw_time.value()
    nr_of_averages = ui.spinBox_conf_averages.value()
    save_loc = ui.lineEdit_conf_data_loc.text()

    save_period_seconds = ui.timeEdit_conf_save_period.time()
    save_period_seconds = save_period_seconds.minute() * 60 + \
        save_period_seconds.second()

    save_type = ui.comboBox_conf_save_type.currentText()
    port_name = ui.comboBox_conf_Port_name.currentText()

    logger.info("Have configuration data")

    new_configuration_data = ConfigurationData(
        akw_time, nr_of_averages, save_period_seconds, save_loc, save_type, port_name)
    current_configuration_data.update_and_drop_diferances(
        new_configuration_data)
    current_configuration_data = new_configuration_data


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
