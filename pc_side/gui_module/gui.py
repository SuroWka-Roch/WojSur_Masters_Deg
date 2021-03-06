# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './desiner_resorces/counter.ui'
#
# Created by: PyQt5 UI code generator 5.12.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(975, 662)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/monitor-icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.Configuration = QtWidgets.QWidget()
        self.Configuration.setObjectName("Configuration")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.Configuration)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.spinBox_conf_averages = QtWidgets.QSpinBox(self.Configuration)
        self.spinBox_conf_averages.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_conf_averages.setProperty("value", 1)
        self.spinBox_conf_averages.setObjectName("spinBox_conf_averages")
        self.gridLayout_2.addWidget(self.spinBox_conf_averages, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 10, 3, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 10, 2, 1, 1)
        self.pushButton_conf_Set_configuration = QtWidgets.QPushButton(self.Configuration)
        self.pushButton_conf_Set_configuration.setObjectName("pushButton_conf_Set_configuration")
        self.gridLayout_2.addWidget(self.pushButton_conf_Set_configuration, 11, 1, 1, 1)
        self.label_20 = QtWidgets.QLabel(self.Configuration)
        self.label_20.setObjectName("label_20")
        self.gridLayout_2.addWidget(self.label_20, 8, 1, 1, 1)
        self.pushButton_conf_reset_port_list = QtWidgets.QPushButton(self.Configuration)
        self.pushButton_conf_reset_port_list.setObjectName("pushButton_conf_reset_port_list")
        self.gridLayout_2.addWidget(self.pushButton_conf_reset_port_list, 6, 2, 1, 1)
        self.label_18 = QtWidgets.QLabel(self.Configuration)
        self.label_18.setObjectName("label_18")
        self.gridLayout_2.addWidget(self.label_18, 6, 1, 1, 1)
        self.pushButton_conf_stop = QtWidgets.QPushButton(self.Configuration)
        self.pushButton_conf_stop.setObjectName("pushButton_conf_stop")
        self.gridLayout_2.addWidget(self.pushButton_conf_stop, 11, 2, 1, 1)
        self.label_save_period = QtWidgets.QLabel(self.Configuration)
        self.label_save_period.setObjectName("label_save_period")
        self.gridLayout_2.addWidget(self.label_save_period, 3, 1, 1, 1)
        self.label_19 = QtWidgets.QLabel(self.Configuration)
        self.label_19.setAlignment(QtCore.Qt.AlignCenter)
        self.label_19.setObjectName("label_19")
        self.gridLayout_2.addWidget(self.label_19, 7, 1, 1, 3)
        self.label_averages = QtWidgets.QLabel(self.Configuration)
        self.label_averages.setObjectName("label_averages")
        self.gridLayout_2.addWidget(self.label_averages, 1, 1, 1, 1)
        self.timeEdit_conf_save_period = QtWidgets.QTimeEdit(self.Configuration)
        self.timeEdit_conf_save_period.setCurrentSection(QtWidgets.QDateTimeEdit.MinuteSection)
        self.timeEdit_conf_save_period.setTime(QtCore.QTime(0, 10, 0))
        self.timeEdit_conf_save_period.setObjectName("timeEdit_conf_save_period")
        self.gridLayout_2.addWidget(self.timeEdit_conf_save_period, 3, 3, 1, 1)
        self.lineEdit_conf_data_loc = QtWidgets.QLineEdit(self.Configuration)
        font = QtGui.QFont()
        font.setItalic(True)
        self.lineEdit_conf_data_loc.setFont(font)
        self.lineEdit_conf_data_loc.setFrame(True)
        self.lineEdit_conf_data_loc.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lineEdit_conf_data_loc.setPlaceholderText("")
        self.lineEdit_conf_data_loc.setObjectName("lineEdit_conf_data_loc")
        self.gridLayout_2.addWidget(self.lineEdit_conf_data_loc, 4, 3, 1, 1)
        self.spinBox_conf_akw_time = QtWidgets.QSpinBox(self.Configuration)
        self.spinBox_conf_akw_time.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_conf_akw_time.setMaximum(100000)
        self.spinBox_conf_akw_time.setProperty("value", 1000)
        self.spinBox_conf_akw_time.setObjectName("spinBox_conf_akw_time")
        self.gridLayout_2.addWidget(self.spinBox_conf_akw_time, 0, 3, 1, 1)
        self.comboBox_Low_Rate = QtWidgets.QComboBox(self.Configuration)
        self.comboBox_Low_Rate.setObjectName("comboBox_Low_Rate")
        self.comboBox_Low_Rate.addItem("")
        self.comboBox_Low_Rate.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_Low_Rate, 8, 3, 1, 1)
        self.label_akw_time = QtWidgets.QLabel(self.Configuration)
        self.label_akw_time.setObjectName("label_akw_time")
        self.gridLayout_2.addWidget(self.label_akw_time, 0, 1, 1, 1)
        self.comboBox_conf_save_type = QtWidgets.QComboBox(self.Configuration)
        self.comboBox_conf_save_type.setObjectName("comboBox_conf_save_type")
        self.comboBox_conf_save_type.addItem("")
        self.comboBox_conf_save_type.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_conf_save_type, 5, 3, 1, 1)
        self.label_data_location = QtWidgets.QLabel(self.Configuration)
        self.label_data_location.setObjectName("label_data_location")
        self.gridLayout_2.addWidget(self.label_data_location, 4, 1, 1, 1)
        self.pushButton_conf_start = QtWidgets.QPushButton(self.Configuration)
        self.pushButton_conf_start.setObjectName("pushButton_conf_start")
        self.gridLayout_2.addWidget(self.pushButton_conf_start, 11, 3, 1, 1)
        self.pushButton_conf_Force_save = QtWidgets.QPushButton(self.Configuration)
        self.pushButton_conf_Force_save.setObjectName("pushButton_conf_Force_save")
        self.gridLayout_2.addWidget(self.pushButton_conf_Force_save, 3, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.Configuration)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 5, 1, 1, 1)
        self.comboBox_conf_Port_name = QtWidgets.QComboBox(self.Configuration)
        self.comboBox_conf_Port_name.setObjectName("comboBox_conf_Port_name")
        self.gridLayout_2.addWidget(self.comboBox_conf_Port_name, 6, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 10, 1, 1, 1)
        self.toolButton_conf_log_file_location = QtWidgets.QToolButton(self.Configuration)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_conf_log_file_location.sizePolicy().hasHeightForWidth())
        self.toolButton_conf_log_file_location.setSizePolicy(sizePolicy)
        self.toolButton_conf_log_file_location.setMinimumSize(QtCore.QSize(0, 0))
        self.toolButton_conf_log_file_location.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolButton_conf_log_file_location.setAutoFillBackground(False)
        self.toolButton_conf_log_file_location.setObjectName("toolButton_conf_log_file_location")
        self.gridLayout_2.addWidget(self.toolButton_conf_log_file_location, 4, 2, 1, 1, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        self.label_21 = QtWidgets.QLabel(self.Configuration)
        self.label_21.setObjectName("label_21")
        self.gridLayout_2.addWidget(self.label_21, 9, 1, 1, 1)
        self.comboBox_ENBLR = QtWidgets.QComboBox(self.Configuration)
        self.comboBox_ENBLR.setObjectName("comboBox_ENBLR")
        self.comboBox_ENBLR.addItem("")
        self.comboBox_ENBLR.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_ENBLR, 9, 3, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.Configuration, "")
        self.Data = QtWidgets.QWidget()
        self.Data.setObjectName("Data")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Data)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_8 = QtWidgets.QLabel(self.Data)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.lcdNumber_7 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_7.setDigitCount(7)
        self.lcdNumber_7.setObjectName("lcdNumber_7")
        self.gridLayout.addWidget(self.lcdNumber_7, 6, 1, 1, 1)
        self.lcdNumber_4 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_4.setDigitCount(7)
        self.lcdNumber_4.setObjectName("lcdNumber_4")
        self.gridLayout.addWidget(self.lcdNumber_4, 3, 1, 1, 1)
        self.label_16 = QtWidgets.QLabel(self.Data)
        self.label_16.setObjectName("label_16")
        self.gridLayout.addWidget(self.label_16, 7, 2, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.Data)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 2, 2, 1, 1)
        self.lcdNumber_8 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_8.setDigitCount(7)
        self.lcdNumber_8.setObjectName("lcdNumber_8")
        self.gridLayout.addWidget(self.lcdNumber_8, 7, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.Data)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.Data)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.lcdNumber_6 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_6.setDigitCount(7)
        self.lcdNumber_6.setObjectName("lcdNumber_6")
        self.gridLayout.addWidget(self.lcdNumber_6, 5, 1, 1, 1)
        self.lcdNumber_1 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_1.setDigitCount(7)
        self.lcdNumber_1.setObjectName("lcdNumber_1")
        self.gridLayout.addWidget(self.lcdNumber_1, 0, 1, 1, 1)
        self.lcdNumber_5 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_5.setDigitCount(7)
        self.lcdNumber_5.setObjectName("lcdNumber_5")
        self.gridLayout.addWidget(self.lcdNumber_5, 4, 1, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.Data)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 3, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.Data)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 1, 2, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.Data)
        self.label_14.setObjectName("label_14")
        self.gridLayout.addWidget(self.label_14, 5, 2, 1, 1)
        self.lcdNumber_2 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_2.setDigitCount(7)
        self.lcdNumber_2.setObjectName("lcdNumber_2")
        self.gridLayout.addWidget(self.lcdNumber_2, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.Data)
        self.label_13.setObjectName("label_13")
        self.gridLayout.addWidget(self.label_13, 4, 2, 1, 1)
        self.label_1 = QtWidgets.QLabel(self.Data)
        self.label_1.setObjectName("label_1")
        self.gridLayout.addWidget(self.label_1, 0, 0, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.Data)
        self.label_15.setObjectName("label_15")
        self.gridLayout.addWidget(self.label_15, 6, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.Data)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.Data)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.Data)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.Data)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.Data)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.lcdNumber_3 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_3.setDigitCount(7)
        self.lcdNumber_3.setObjectName("lcdNumber_3")
        self.gridLayout.addWidget(self.lcdNumber_3, 2, 1, 1, 1)
        self.lcdNumber_9 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_9.setDigitCount(7)
        self.lcdNumber_9.setObjectName("lcdNumber_9")
        self.gridLayout.addWidget(self.lcdNumber_9, 0, 3, 1, 1)
        self.lcdNumber_10 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_10.setDigitCount(7)
        self.lcdNumber_10.setObjectName("lcdNumber_10")
        self.gridLayout.addWidget(self.lcdNumber_10, 1, 3, 1, 1)
        self.lcdNumber_11 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_11.setDigitCount(7)
        self.lcdNumber_11.setObjectName("lcdNumber_11")
        self.gridLayout.addWidget(self.lcdNumber_11, 2, 3, 1, 1)
        self.lcdNumber_12 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_12.setDigitCount(7)
        self.lcdNumber_12.setObjectName("lcdNumber_12")
        self.gridLayout.addWidget(self.lcdNumber_12, 3, 3, 1, 1)
        self.lcdNumber_13 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_13.setDigitCount(7)
        self.lcdNumber_13.setObjectName("lcdNumber_13")
        self.gridLayout.addWidget(self.lcdNumber_13, 4, 3, 1, 1)
        self.lcdNumber_14 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_14.setDigitCount(7)
        self.lcdNumber_14.setObjectName("lcdNumber_14")
        self.gridLayout.addWidget(self.lcdNumber_14, 5, 3, 1, 1)
        self.lcdNumber_15 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_15.setDigitCount(7)
        self.lcdNumber_15.setObjectName("lcdNumber_15")
        self.gridLayout.addWidget(self.lcdNumber_15, 6, 3, 1, 1)
        self.lcdNumber_16 = QtWidgets.QLCDNumber(self.Data)
        self.lcdNumber_16.setDigitCount(7)
        self.lcdNumber_16.setObjectName("lcdNumber_16")
        self.gridLayout.addWidget(self.lcdNumber_16, 7, 3, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.tabWidget.addTab(self.Data, "")
        self.Visualisation = QtWidgets.QWidget()
        self.Visualisation.setObjectName("Visualisation")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.Visualisation)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.frame_vis_fig = QtWidgets.QFrame(self.Visualisation)
        self.frame_vis_fig.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_vis_fig.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_vis_fig.setObjectName("frame_vis_fig")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_vis_fig)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.grid_vis_fig = QtWidgets.QGridLayout()
        self.grid_vis_fig.setObjectName("grid_vis_fig")
        self.horizontalLayout_4.addLayout(self.grid_vis_fig)
        self.gridLayout_4.addWidget(self.frame_vis_fig, 0, 0, 1, 3)
        self.checkBox_vis_logscale = QtWidgets.QCheckBox(self.Visualisation)
        self.checkBox_vis_logscale.setObjectName("checkBox_vis_logscale")
        self.gridLayout_4.addWidget(self.checkBox_vis_logscale, 1, 2, 1, 1)
        self.pushButton_vis_refresh = QtWidgets.QPushButton(self.Visualisation)
        self.pushButton_vis_refresh.setObjectName("pushButton_vis_refresh")
        self.gridLayout_4.addWidget(self.pushButton_vis_refresh, 1, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem3, 1, 1, 1, 1)
        self.tabWidget.addTab(self.Visualisation, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.tab)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.Put_fig_here_OneShot = QtWidgets.QFrame(self.tab)
        self.Put_fig_here_OneShot.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Put_fig_here_OneShot.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Put_fig_here_OneShot.setObjectName("Put_fig_here_OneShot")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.Put_fig_here_OneShot)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.grid_ss_fig = QtWidgets.QGridLayout()
        self.grid_ss_fig.setObjectName("grid_ss_fig")
        self.horizontalLayout_5.addLayout(self.grid_ss_fig)
        self.gridLayout_5.addWidget(self.Put_fig_here_OneShot, 0, 0, 1, 4)
        self.lineEdit_ss_file_loc = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_ss_file_loc.setObjectName("lineEdit_ss_file_loc")
        self.gridLayout_5.addWidget(self.lineEdit_ss_file_loc, 3, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.tab)
        self.label_17.setObjectName("label_17")
        self.gridLayout_5.addWidget(self.label_17, 4, 0, 1, 1)
        self.toolButton_ss_save_loc = QtWidgets.QToolButton(self.tab)
        self.toolButton_ss_save_loc.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_ss_save_loc.sizePolicy().hasHeightForWidth())
        self.toolButton_ss_save_loc.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setStyleStrategy(QtGui.QFont.PreferDefault)
        self.toolButton_ss_save_loc.setFont(font)
        self.toolButton_ss_save_loc.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.toolButton_ss_save_loc.setArrowType(QtCore.Qt.NoArrow)
        self.toolButton_ss_save_loc.setObjectName("toolButton_ss_save_loc")
        self.gridLayout_5.addWidget(self.toolButton_ss_save_loc, 3, 3, 1, 1)
        self.OneShot_save_loc_label = QtWidgets.QLabel(self.tab)
        self.OneShot_save_loc_label.setObjectName("OneShot_save_loc_label")
        self.gridLayout_5.addWidget(self.OneShot_save_loc_label, 3, 0, 1, 1)
        self.spinBox_ss_akw_time = QtWidgets.QSpinBox(self.tab)
        self.spinBox_ss_akw_time.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spinBox_ss_akw_time.setMinimum(1)
        self.spinBox_ss_akw_time.setMaximum(1000000)
        self.spinBox_ss_akw_time.setProperty("value", 1000)
        self.spinBox_ss_akw_time.setObjectName("spinBox_ss_akw_time")
        self.gridLayout_5.addWidget(self.spinBox_ss_akw_time, 4, 2, 1, 1)
        self.pushButton_ss_run = QtWidgets.QPushButton(self.tab)
        self.pushButton_ss_run.setObjectName("pushButton_ss_run")
        self.gridLayout_5.addWidget(self.pushButton_ss_run, 7, 0, 1, 4)
        self.checkBox_logscale_OneShot = QtWidgets.QCheckBox(self.tab)
        self.checkBox_logscale_OneShot.setObjectName("checkBox_logscale_OneShot")
        self.gridLayout_5.addWidget(self.checkBox_logscale_OneShot, 4, 3, 1, 1)
        self.horizontalLayout_3.addLayout(self.gridLayout_5)
        self.tabWidget.addTab(self.tab, "")
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Counter Program"))
        self.pushButton_conf_Set_configuration.setText(_translate("MainWindow", "Set configuration"))
        self.label_20.setText(_translate("MainWindow", "Low Rate"))
        self.pushButton_conf_reset_port_list.setText(_translate("MainWindow", "Reset ports list"))
        self.label_18.setText(_translate("MainWindow", "Arduino Port"))
        self.pushButton_conf_stop.setText(_translate("MainWindow", "Stop"))
        self.label_save_period.setText(_translate("MainWindow", "Auto save period [mm:ss]"))
        self.label_19.setText(_translate("MainWindow", "Integrator Control"))
        self.label_averages.setText(_translate("MainWindow", "Nr of avrerages"))
        self.timeEdit_conf_save_period.setDisplayFormat(_translate("MainWindow", "mm:ss"))
        self.lineEdit_conf_data_loc.setText(_translate("MainWindow", "./data/"))
        self.comboBox_Low_Rate.setItemText(0, _translate("MainWindow", "Low"))
        self.comboBox_Low_Rate.setItemText(1, _translate("MainWindow", "High"))
        self.label_akw_time.setText(_translate("MainWindow", "Acquisition time [ms]"))
        self.comboBox_conf_save_type.setItemText(0, _translate("MainWindow", "JSON"))
        self.comboBox_conf_save_type.setItemText(1, _translate("MainWindow", "CSV"))
        self.label_data_location.setText(_translate("MainWindow", "Data location"))
        self.pushButton_conf_start.setText(_translate("MainWindow", "Start"))
        self.pushButton_conf_Force_save.setText(_translate("MainWindow", "Force save now"))
        self.label.setText(_translate("MainWindow", "Data save type"))
        self.toolButton_conf_log_file_location.setText(_translate("MainWindow", "Log file location"))
        self.label_21.setText(_translate("MainWindow", "ENBLR"))
        self.comboBox_ENBLR.setItemText(0, _translate("MainWindow", "Low"))
        self.comboBox_ENBLR.setItemText(1, _translate("MainWindow", "High"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Configuration), _translate("MainWindow", "Configuration"))
        self.label_8.setText(_translate("MainWindow", "TextLabel"))
        self.label_16.setText(_translate("MainWindow", "TextLabel"))
        self.label_11.setText(_translate("MainWindow", "TextLabel"))
        self.label_5.setText(_translate("MainWindow", "TextLabel"))
        self.label_6.setText(_translate("MainWindow", "TextLabel"))
        self.label_12.setText(_translate("MainWindow", "TextLabel"))
        self.label_10.setText(_translate("MainWindow", "TextLabel"))
        self.label_14.setText(_translate("MainWindow", "TextLabel"))
        self.label_13.setText(_translate("MainWindow", "TextLabel"))
        self.label_1.setText(_translate("MainWindow", "TextLabel"))
        self.label_15.setText(_translate("MainWindow", "TextLabel"))
        self.label_9.setText(_translate("MainWindow", "TextLabel"))
        self.label_2.setText(_translate("MainWindow", "TextLabel"))
        self.label_4.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "TextLabel"))
        self.label_7.setText(_translate("MainWindow", "TextLabel"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Data), _translate("MainWindow", "Data"))
        self.checkBox_vis_logscale.setText(_translate("MainWindow", "Logaritmic scale"))
        self.pushButton_vis_refresh.setText(_translate("MainWindow", "Refresh "))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Visualisation), _translate("MainWindow", "Visualisation"))
        self.lineEdit_ss_file_loc.setText(_translate("MainWindow", "./data/SingleShot/"))
        self.label_17.setText(_translate("MainWindow", "Acquisition time [ms]"))
        self.toolButton_ss_save_loc.setText(_translate("MainWindow", "Log file location"))
        self.OneShot_save_loc_label.setText(_translate("MainWindow", "Save location"))
        self.pushButton_ss_run.setText(_translate("MainWindow", "Run"))
        self.checkBox_logscale_OneShot.setText(_translate("MainWindow", "Logaritmic scale"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Single Shot"))
import gui_module.resorce_rc
