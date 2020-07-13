#!/usr/bin/env python3.7

import sys
import logging
from PyQt5 import QtWidgets, QtCore

from serial import SerialException, serialutil
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

from backend_module.back_end import CountRateData, rawLogClass, back_end_deamon, CountRateDataSingleShoot
from backend_module.back_end import ExpectedResponseNotFound, NoReadyToResponse, CommunicationError
from backend_module.back_end import update_count_data
from backend_module.configuration import REPEAT_FOR, DEAMON_LOOP_COUNT, SLEEP_TIME

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

    except serialutil.SerialException as e:
        if not silence:
            popup_window("resorce busy wait a moment and try again")

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
    get_vis_configuration_info(ui, current_configuration_data, count_data)

    #fix a bug conserning changind akw time and visualisation
    if current_configuration_data["akw_time"] != count_data.akw_time:
        count_data.set_vis_to_now()

    count_data.set_akw_time(current_configuration_data["akw_time"])
    count_data.change_nr_of_averages(current_configuration_data["nr_of_averages"])
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

    ui.checkBox_vis_logscale.stateChanged.connect(
        lambda: change_log_scale_vis(current_configuration_data))

    ui.checkBox_logscale_OneShot.stateChanged.connect(ui.ss_fig.change_scale)

    ui.pushButton_ss_run.clicked.connect(lambda: ss_run_buttom_function(
        ui, serial_port, log, semaphore, current_configuration_data, count_data, save_data_timer))
    
    ui.pushButton_vis_refresh.clicked.connect(lambda: count_data.set_vis_to_now())


def ss_run_buttom_function(ui, serial_port, log, port_semaphore, current_configuration_data, count_data, save_data_timer):
    if current_configuration_data.empty:
        configuration_buttom_func(ui, current_configuration_data,
                                  serial_port, log, port_semaphore, count_data, save_data_timer)

    if "SS_deamon" in [thread.getName() for thread in threading.enumerate()]:
        popup_window("Wait for previous run to end")
        return

    stop_buttom_function(port_semaphore, serial_port,
                         current_configuration_data, log)

    save_location, akw_time = get_SingleShot_configuration_info(ui)

    ss_count_data = CountRateDataSingleShoot(CANAL_NAMES, akw_time)

    SS_thread = threading.Thread(target=SS_deamon, args=(
        ui, serial_port, port_semaphore, log, ss_count_data,save_location), name="SS_deamon", daemon=True)

    SS_thread.start()



def SS_deamon(ui, serial_port, port_semaphore, log, ss_count_data, save_location):
    backend_module.back_end.get_ss_mesurement(
        serial_port, port_semaphore, log, ss_count_data)
    ui.ss_fig.update_figure(CANAL_NAMES,ss_count_data.data_for_plot())
    logger.debug("Single Shot result for canals of:\n{}\n{}".format(
        CANAL_NAMES, ss_count_data.data_for_plot()))
    
    save_config = ConfigurationData(ss_count_data.akw_time,0,0,save_location,"Exel compliant", 0)
    save_data(ss_count_data, save_config)


def change_log_scale_vis(current_configuration_data):
    current_configuration_data["vis_log_scale"] = not current_configuration_data["vis_log_scale"]


def start_buttom_function(ui, current_configuration_data, count_data, semaphore, serial_port, log, save_data_timer):
    # if current_configuration_data.empty:
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


def run_window():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    # ui = gui_module.gui.Ui_MainWindow()
    ui = gui_module.fig.MyWindowWithFig()
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
    update_count_data_timer.start(100)

    save_data_timer = QtCore.QTimer()
    save_data_timer.timeout.connect(lambda: save_data(
        count_data, current_configuration_data))
    save_data_timer.start(600 * 1000)

    update_vis_timer = QtCore.QTimer()
    update_vis_timer.timeout.connect(lambda: update_figure(
        ui, count_data, current_configuration_data))
    update_vis_timer.start(gui_module.configuration.GUI_UPDATE_PERIOD_MS)

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
    save_data(count_data, current_configuration_data, silence=True)
    with open("./log.txt", "w") as log_file:
        log_file.write(str(log))


def raw_data_function(count_data, displays):
    values = count_data.last_values()
    for num, display in enumerate(displays):
        display.display(values[num])


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        logger.info("Making directory for cur date")
        os.makedirs(directory)


def save_data(count_data, current_configuration_data, silence=False):
    if current_configuration_data.empty and not silence:
        popup_window("Set configuration before saving")
        return
    now = datetime.now()
    file_name = now.strftime("%H:%M ")

    if silence and current_configuration_data.empty:
        directory = os.path.join(
            ".", "panic data dump", now.strftime("%d-%m-%Y"))
        file_save_type = "JSON"
    else:
        directory = os.path.join(
            current_configuration_data["save_location"], now.strftime("%d-%m-%Y"))
        file_save_type = current_configuration_data["save_type"]
        file_name += str(current_configuration_data["akw_time"]) + "[ms]"
    file_path = os.path.join(directory, file_name)
    ensure_dir(file_path)

    if file_save_type == "JSON":
        file_path += ".JSON"
        count_data.JSON_dump_to(file_path)
    else:
        file_path += ".csv"
        count_data.CSV_dump_to(file_path)

    count_data.clear()
    logger.info("file {} saved".format(file_path))


def update_figure(ui, count_rate_data, current_configuration_data):
    labels, x, y = count_rate_data.data_for_plot()
    if labels == None:
        return

    ui.vis_fig.update_figure(
        labels, x, y, log_scale=current_configuration_data["vis_log_scale"])


def create_backend_deamon(count_rate_data, semaphore, log, serial_port):
    thread = threading.Thread(target=back_end_deamon, args=(
        count_rate_data, semaphore, log, serial_port), daemon=True, name="SerialReader")
    return thread


def get_vis_configuration_info(ui, current_configuration_data, count_data):
    akw_time = ui.spinBox_conf_akw_time.value()
    nr_of_averages = ui.spinBox_conf_averages.value()
    save_loc = ui.lineEdit_conf_data_loc.text()

    save_period_seconds = ui.timeEdit_conf_save_period.time()
    save_period_seconds = save_period_seconds.minute() * 60 + \
        save_period_seconds.second()

    save_type = ui.comboBox_conf_save_type.currentText()
    port_name = ui.comboBox_conf_Port_name.currentText()

    logger.info("Have configuration data")

    old_configuration_data = deepcopy(current_configuration_data)

    new_configuration_data = ConfigurationData(
        akw_time, nr_of_averages, save_period_seconds, save_loc, save_type, port_name)
    differences = current_configuration_data.update_and_drop_diferances(
        new_configuration_data)

    if "akw_time" in differences and not count_data.is_empty():
        save_data(count_data, old_configuration_data, silence=True)
        count_data.clear()

    # current_configuration_data = new_configuration_data


def get_SingleShot_configuration_info(ui):
    file_loc = ui.lineEdit_ss_file_loc.text()
    akw_time = ui.spinBox_ss_akw_time.value()

    return file_loc, akw_time


#simple logging global logger
logger = set_logger()

if __name__ == "__main__":
    run_window()
    logger.info("App closings")
    sys.exit()
