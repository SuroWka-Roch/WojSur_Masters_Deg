"""
================
Embedding In QT5
================

Simple Qt5 application embedding Matplotlib canvases

Copyright (C) 2005 Florent Rougon
              2006 Darren Dale
              2015 Jens H Nielsen

This file is an example program for Matplotlib. It may be used and
modified with no restriction; raw copies as well as modified versions
may be distributed without limitation.
"""

from __future__ import unicode_literals
import gui_module.gui
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from numpy import arange, sin, pi
from PyQt5 import QtCore, QtWidgets
import sys
import os
import random
import matplotlib
# Make sure that we are using QT5
matplotlib.use('Qt5Agg')
# Uncomment this line before running, it breaks sphinx-gallery builds


progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.fig.set_label("plis")

    def compute_initial_figure(self):
        pass


class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""

    def compute_initial_figure(self):
        t = arange(0.0, 3.0, 0.01)
        s = sin(2*pi*t)
        self.axes.plot(t, s)


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.axes.plot([0], [0], 'r')
        self.axes.text(-0.01, 0, "Waiting for data")
        self.axes.set_xlabel("Relative time [s]")
        self.axes.set_ylabel("Count rate [Hz]")

    def update_figure(self, labels, x, list_of_y, log_scale=False):
        self.axes.cla()
        self.axes.set_xlabel("Relative time [s]")
        self.axes.set_ylabel("Count rate [Hz]")
        if log_scale:
            self.axes.set_yscale("log")
        for label, y in zip(labels, list_of_y):
            self.axes.plot(x, y, label=label)
        self.axes.legend(loc=2)
        self.draw()


class MyDynamicMplCanvasSS(MyMplCanvas):

    def __init__(self, *args, **kwargs):
        self.bar_width = 0.35  # the width of the bars
        self.log_scale = False
        self.current_data = [1,2]
        self.current_labels = ["you shuld not see this","lol"]

        MyMplCanvas.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        self.axes.text(0.4, 0.5, "Waiting for data")
        self.axes.set_xlabel("Canals")
        self.axes.set_ylabel("Count rate [Hz]")

    def update_figure(self, labels, y):
        self.axes.cla()
        self.axes.set_xlabel("Channels")
        self.axes.set_ylabel("Count rate [Hz]")

        self.current_labels = labels
        self.current_data = y

        x = arange(len(labels))

        self.axes.set_xticks(x)
        self.axes.set_xticklabels(labels)


        if self.log_scale:
            self.axes.set_yscale("log")
        else:
            self.axes.set_yscale("linear")

        self.axes.bar(x,y,self.bar_width)
        self.draw()

    def change_scale(self):
        if self.log_scale:
            self.log_scale = False
        else:
            self.log_scale = True
        
        self.update_figure(self.current_labels, self.current_data)


class MyWindowWithFig(gui_module.gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.ss_fig = None
        self.vis_fig = None

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.ss_fig = MyDynamicMplCanvasSS(
            self.frame_vis_fig, width=5, height=4, dpi=100)
        self.vis_fig = MyDynamicMplCanvas(
            self.Put_fig_here_OneShot, width=5, height=4, dpi=100)
        self.grid_vis_fig.addWidget(self.vis_fig)
        self.grid_ss_fig.addWidget(self.ss_fig)
