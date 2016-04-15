import os
import sys
import collections
import pyqtgraph as pg
import numpy as np
from pyqtgraph.Qt import QtCore, QtGui, uic
from datetime import datetime
#import hardwareADCread
import methods

#########################
## EKG UI              ##
#########################
class ekgui(QtGui.QMainWindow):
    def __init__(self, sampleinterval=0.02, timewindow=10):
        # Data stuff
        self.updaterate = sampleinterval*100     #timer triggering rate (ms)
        self._interval = int(sampleinterval*1000)
        self._bufsize = int(timewindow/sampleinterval)
        self.buffer = collections.deque([0.0]*self._bufsize, self._bufsize) #buffer for displayed data
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)
        self.session = session()    #assign default session

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
        val = methods.sample()
        self.buffer.append(val)
        if(self.session.recording):
            self.session.data.append(val)
        self.y[:] = self.buffer
        self.curve.setData(self.x, self.y)
        self.app.processEvents()

    def save(self):
        self.session.save()

    def load(self):
        self.session.load()
        time = np.linspace(-(float(self.session.data.size)/self._bufsize)*10, 0.0, self.session.data.size)
        self.curve.setData(time, self.session.data)
        self.app.processEvents()

#########################
## Options screen      ##
#########################
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

#########################
## Sessions            ##
#########################
class session:
    def __init__(self):
        self.patient = ''
        self.timestamp = ''
        self.recording = False
        self.data = collections.deque()

    #create or assign (existing) session
    def new(self, patient, timestamp = datetime.now()):
        self.patient = patient
        self.timestamp = timestamp
        self.recording = True

    def save(self):
        methods.save_ses(self.patient, self.timestamp, np.array(self.data))

    def load(self):
        self.data = methods.load_ses(self.patient)
