from PyQt5.QtWidgets import QFileDialog


def setup_names(ui):
    CANAL_NAMES = ["1A1","1A2","1A3","1A4","1A5","1A6","1A7","1A8","2A1","2A2","2A3","2A4","2A5","2A6","2A7","2A8"]
    for i in range(1,17):
        exec("ui.label_" + str(i) + ".setText('" + CANAL_NAMES[i-1] + "')")

def fileselect():
    return QFileDialog.getExistingDirectory()

def set_conf_file_loc(ui):
    ui.lineEdit_conf_data_loc.setText(fileselect())

def set_ss_file_loc(ui):
    ui.lineEdit_ss_file_loc.setText(fileselect())

def test():
    print("aaa")

def my_setup(ui):
    setup_names(ui)
    ui.toolButton_conf_log_file_location.clicked.connect(lambda: set_conf_file_loc(ui))
    ui.toolButton_ss_save_loc.clicked.connect(lambda: set_ss_file_loc(ui))