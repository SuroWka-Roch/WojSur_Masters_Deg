from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore, QtWidgets
import gui_module.fig as fig
from gui_module.serialInfo import serial_ports
from gui_module.configuration import CANAL_NAMES


def get_counter_list():
    counter_list = []
    for i in range(1, 17):
        exec("counter_list.append( ui.label_" + str(i) + ")")

    return counter_list


def setup_names(ui):
    for i in range(1, 17):
        exec("ui.label_" + str(i) + ".setText('" + CANAL_NAMES[i-1] + "')")


def fileselect():
    return QFileDialog.getExistingDirectory()


def set_conf_file_loc(ui):
    ui.lineEdit_conf_data_loc.setText(fileselect())


def set_ss_file_loc(ui):
    ui.lineEdit_ss_file_loc.setText(fileselect())


def my_setup(ui):
    setup_names(ui)
    ui.toolButton_conf_log_file_location.clicked.connect(
        lambda: set_conf_file_loc(ui))
    ui.toolButton_ss_save_loc.clicked.connect(lambda: set_ss_file_loc(ui))
    insert_plot(ui)
    set_port_combobox(ui)
    ui.pushButton_conf_reset_port_list.clicked.connect(
        lambda: set_port_combobox(ui))


def set_port_combobox(ui):
    portlist = serial_ports()
    ui.comboBox_conf_Port_name.clear()

    if portlist:
        for port_name in portlist:
            ui.comboBox_conf_Port_name.addItem(port_name)
    else:
        ui.comboBox_conf_Port_name.addItem("Not connected")


def insert_plot(ui):
    ss_fig = fig.MyStaticMplCanvas(
        ui.frame_vis_fig, width=5, height=4, dpi=100)
    vis_fig = fig.MyDynamicMplCanvas(
        ui.Put_fig_here_OneShot, width=5, height=4, dpi=100)
    ui.grid_vis_fig.addWidget(vis_fig)
    ui.grid_ss_fig.addWidget(ss_fig)


def get_digital_numbers(ui):
    numer_list = [ui.lcdNumber_1,
                  ui.lcdNumber_2,
                  ui.lcdNumber_3,
                  ui.lcdNumber_4,
                  ui.lcdNumber_5,
                  ui.lcdNumber_6,
                  ui.lcdNumber_7,
                  ui.lcdNumber_8,
                  ui.lcdNumber_9,
                  ui.lcdNumber_10,
                  ui.lcdNumber_11,
                  ui.lcdNumber_12,
                  ui.lcdNumber_13,
                  ui.lcdNumber_14,
                  ui.lcdNumber_15,
                  ui.lcdNumber_16]
    return numer_list
