#!/usr/bin/env python3.7

import sys
import logging
from PyQt5 import QtWidgets, QtCore

from serial import SerialException
from serial import Serial

import time
import threading

import os

import gui_module.my_gui_setup
import gui_module.gui as gui

from gui_module.configuration import CANAL_NAMES


import backend_module.comunication
from backend_module.back_end import ConfigurationData
from copy import deepcopy

from backend_module.back_end import CountRateData, rawLogClass, back_end_deamon
from backend_module.back_end import ExpectedResponseNotFound, NoReadyToResponse, CommunicationError
from backend_module.configuration import REPEAT_FOR

from datetime import datetime


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


def configure_arduino(serial_port, current_configuration_data, log, silence=False):
    return comunication_function_hendler_funtion(lambda: backend_module.comunication.configure_all(
        serial_port, current_configuration_data, log), silence=silence)


def popup_window(msg):
    error_dialog = QtWidgets.QErrorMessage()
    error_dialog.showMessage(msg)
    error_dialog.exec_()


def comunication_function_hendler_funtion(fun, silence=False):
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


def try_port(SerialPort, current_configuration_data, silence=False):
    port_name = current_configuration_data.data["port_name"]
    return comunication_function_hendler_funtion(lambda: backend_module.comunication.try_port(port_name, SerialPort), silence=silence)


def configuration_buttom_func(ui, current_configuration_data, serial_port, log, semaphore, count_data, save_data_timer):
    get_vis_configuration_info(ui, current_configuration_data)
    count_data.set_akw_time(current_configuration_data["akw_time"])
    save_data_timer.setInterval(
        current_configuration_data["save_period"] * 1000)
    logger.debug(current_configuration_data)
    logger.debug(serial_port)
    if current_configuration_data["port_name"] == "Not connected":
        popup_window("Pick a port")
        return
    with semaphore:
        for tries in range(REPEAT_FOR):
            if try_port(serial_port, current_configuration_data, silence=True if not tries == REPEAT_FOR - 1 else False):
                break
        else:
            return
        for tries in range(REPEAT_FOR):
            if configure_arduino(serial_port, current_configuration_data, log, silence=True if not tries == REPEAT_FOR - 1 else False):
                break
    logger.info("Have connection to serial port:\n{}\nWith setting of:\n{}".format(
        serial_port, current_configuration_data))


def connect_backend(ui, current_configuration_data, serial_port, log, semaphore, count_data, save_data_timer):
    ui.pushButton_conf_Set_configuration.clicked.connect(
        lambda: configuration_buttom_func(ui, current_configuration_data, serial_port, log, semaphore, count_data, save_data_timer))
    ui.pushButton_conf_start.clicked.connect(
        lambda: start_buttom_function(
            ui, current_configuration_data, count_data, semaphore, serial_port, log, save_data_timer)
    )
    ui.pushButton_conf_stop.clicked.connect(lambda: stop_buttom_function(
        semaphore, serial_port, current_configuration_data, log))
    ui.pushButton_conf_Force_save.clicked.connect(
        lambda: save_data(count_data, current_configuration_data))


def start_buttom_function(ui, current_configuration_data, count_data, semaphore, serial_port, log, save_data_timer):
    if current_configuration_data.empty:
        configuration_buttom_func(ui, current_configuration_data,
                                  serial_port, log, semaphore, count_data, save_data_timer)
    with semaphore:
        for tries in range(REPEAT_FOR):
            if comunication_function_hendler_funtion(lambda: backend_module.comunication.start(serial_port, log), silence=True if not tries == REPEAT_FOR - 1 else False):
                break
    logger.info("Started mesurement")


def stop_buttom_function(semaphore, serial_port, current_configuration_data, log):
    if current_configuration_data.empty:
        popup_window("Configuration is not set")
        return
    with semaphore:
        for tries in range(REPEAT_FOR):
            if comunication_function_hendler_funtion(lambda: backend_module.comunication.stop(serial_port, log), silence=True if not tries == REPEAT_FOR - 1 else False):
                break
    logger.info("stoped mesurement")


def update_count_data(count_data, log):
    log_chunk = log.return_chunk()
    data, end_pointer = CountRateData.seperate_data(log_chunk)
    if data:
        count_data.update(data)
        log.set_pointer(end_pointer)


def run_window():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = gui_module.gui.Ui_MainWindow()
    ui.setupUi(MainWindow)
    gui_module.my_gui_setup.my_setup(ui)

    #Value holders
    count_data = CountRateData(CANAL_NAMES, None)
    serial_port = Serial()
    current_configuration_data = ConfigurationData.create_empty()
    log = rawLogClass()
    data = CountRateData(gui_module.configuration.CANAL_NAMES,
                         ui.spinBox_conf_akw_time.value)
    serial_port_semaphore = threading.Semaphore()
    thread = create_backend_deamon(
        data, serial_port_semaphore, log, serial_port)
    thread.start()

    #timers

    update_count_data_timer = QtCore.QTimer()
    update_count_data_timer.timeout.connect(
        lambda: update_count_data(count_data, log))
    update_count_data_timer.start(3000)

    save_data_timer = QtCore.QTimer()
    save_data_timer.timeout.connect(lambda: save_data(
        count_data, current_configuration_data))
    save_data_timer.start(600 * 1000)

    displays = gui_module.my_gui_setup.get_digital_numbers(ui)
    update_displays_timer = QtCore.QTimer()
    update_displays_timer.timeout.connect(
        lambda: raw_data_function(count_data, displays))
    update_displays_timer.start(gui_module.configuration.GUI_UPDATE_PERIOD_MS)

    connect_backend(ui, current_configuration_data, serial_port,
                    log, serial_port_semaphore, count_data, save_data_timer)

    MainWindow.show()
    app.exec()

    #clean up
    save_data(count_data, current_configuration_data)


def raw_data_function(count_data, displays):
    values = count_data.last_values()
    for num, display in enumerate(displays):
        display.display(values[num])


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        logger.info("Making directory for cur date")
        os.makedirs(directory)


def save_data(count_data, current_configuration_data):
    if current_configuration_data.empty:
        popup_window("Set configuration before saving")
        return
    now = datetime.now()
    directory = os.path.join(
        current_configuration_data["save_location"], now.strftime("%d-%m-%Y"))
    file_name = now.strftime("%H:%M ")
    file_name += str(current_configuration_data["akw_time"]) + "[ms]"
    file_path = os.path.join(directory, file_name)
    ensure_dir(file_path)

    if current_configuration_data["save_type"] == "JSON":
        file_path += ".JSON"
        count_data.JSON_dump_to(file_path)
    else:
        file_path += ".csv"
        count_data.CSV_dump_to(file_path)

    count_data.clear()
    logger.info("file saved")


def create_backend_deamon(count_rate_data, semaphore, log, serial_port):
    thread = threading.Thread(target=back_end_deamon, args=(
        count_rate_data, semaphore, log, serial_port), daemon=True, name="reading data")
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
