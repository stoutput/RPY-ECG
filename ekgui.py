import sys
import os
#import spidev
import collections
import time
#import hardwareADCread
import math
import random
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui, uic
from datetime import datetime

class ekgui(QtGui.QMainWindow):
    def __init__(self, sampleinterval=0.02, timewindow=10):
        # Data stuff
        self.updaterate = sampleinterval*100     #timer triggering rate (ms)
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.databuffer = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)

        #init ui
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/ekg.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #init graph
        self.plot = self.ui.graph.getPlotItem()
        self.view = self.plot.getViewBox()
        self.view.setRange(None, (-9,-1), (0.2,3.1), None, True, True)
        self.ui.graph.showGrid(x=True, y=True)
        self.ui.graph.setLabel('left', 'amplitude', 'V')
        self.ui.graph.setLabel('bottom', 'time', 's')
        self.curve = self.graph.plot(self.x, self.y, pen=(255,0,0))

        #timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.getData)

        #connect elements
        self.ui.plotButton.clicked.connect(self.togglePlot)
        self.ui.zoominButton.clicked.connect(self.zoomIn)
        self.ui.zoomoutButton.clicked.connect(self.zoomOut)
        self.ui.optionsButton.clicked.connect(self.newWindow)

        self.ui.showMaximized()

    def newWindow(self):
        self.options = options()

    def zoomIn(self):
        self.view.scaleBy(0.5)

    def zoomOut(self):
        self.view.scaleBy(2.0)

    def togglePlot(self):
        if(self.timer.isActive()):
            self.timer.stop()
            self.ui.plotButton.setText("Start")
        else:
            self.timer.start(self.updaterate)
            self.ui.plotButton.setText("Stop")

    def getData(self):
        self.databuffer.append(sample())
        self.y[:] = self.databuffer
        self.curve.setData(self.x, self.y)
        self.app.processEvents()

class options(QtGui.QWidget):
    kbuttonDown,kbuttonUp,kbuttonRight,kbuttonLeft,kbuttonEsc,kbuttonEnt = QtCore.pyqtSignal(),QtCore.pyqtSignal(),QtCore.pyqtSignal(),QtCore.pyqtSignal(),QtCore.pyqtSignal(),QtCore.pyqtSignal()

    def __init__(self):
        #init window
        QtGui.QWidget.__init__(self)
        self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/options.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        #init buttons
        self.ui.enterButton.clicked.connect(self.enter)
        self.ui.backButton.clicked.connect(self.back)
        self.kbuttonEsc.connect(self.back)
        self.kbuttonEnt.connect(self.enter)

        self.ui.showMaximized()
        self.setFocus()
        self.ui.options.setFocus()

    #triggers keyboard button press events
    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Right:
            self.kbuttonRight.emit()
        elif event.key()==QtCore.Qt.Key_Left:
            self.kbuttonLeft.emit()
        elif event.key()==QtCore.Qt.Key_Up:
            self.kbuttonUp.emit()
        elif event.key()==QtCore.Qt.Key_Down:
            self.kbuttonDown.emit()
        elif event.key()==QtCore.Qt.Key_Escape:
            self.kbuttonEsc.emit()
        elif event.key()==QtCore.Qt.Key_Enter or event.key()==QtCore.Qt.Key_Return:
            self.kbuttonEnt.emit()

    def back(self):
        self.close()

    def enter(self):
        self.close()

def sample():
    frequency = 0.5
    noise = random.normalvariate(0., 1.)
    val = 8.*math.sin(time.time()*frequency*2*math.pi) + noise
    return val

    ##ADC Read
    #value = hardwareADCread.readadc(0)
    #return value

#accepts array as argument (ekgui.data??)
#saves array as a session within user's numpy archive
def save_ses(user, session):
    path = os.path.dirname(os.path.abspath(__file__)) + '/sessions/' + user + datetime.now()

def load_ses(user):
    path = os.path.dirname(os.path.abspath(__file__)) + '/sessions/' + user + datetime.now()

#accepts a plotItem as argument (ekgui.plot)
#saves plot screenshot as png
def save_scr(plot):
    path = os.path.dirname(os.path.abspath(__file__)) + '/screenshots/' + datetime.now()

if __name__ == "__main__":
    #spi = spidev.SpiDev()
    #spi.open(0, 0)
    gui = ekgui()
    #spi.close()
    sys.exit(gui.app.exec_())
