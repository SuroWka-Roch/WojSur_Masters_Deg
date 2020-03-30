#!/usr/bin/env python3.7

import sys
import gui
from PyQt5 import QtWidgets
import my_gui_setup



app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = gui.Ui_MainWindow()
ui.setupUi(MainWindow)

my_gui_setup.my_setup(ui)


MainWindow.show()
sys.exit(app.exec_())