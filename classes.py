# Dependencies
import os
import SolUI
import sys
import collections
import pyqtgraph as pg
import numpy as np
import time
from pyqtgraph.Qt import QtCore, QtGui, uic
from datetime import datetime
import RPi.GPIO as GPIO
from scipy.signal import lfilter, lfilter_zi, iirdesign

# Dependent Scripts
import adc
import methods

#Set Up GPIO Pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_UP)


#########################
## EKG UI              ##
#########################
class ekgui(QtGui.QMainWindow):
    def __init__(self, sampleinterval=0.02, timewindow=10):
        # Data Prep
        self.period = sampleinterval     #sample period in seconds
        self.samplerate = 1/self.period
        self._bufsize = int(timewindow/sampleinterval)
        self.buffer = collections.deque([0.0]*self._bufsize, self._bufsize) #buffer for displayed data
        self.buffer2 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.buffer3 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.buffer4 = collections.deque([0.0]*self._bufsize, self._bufsize)
        self.x = np.linspace(-timewindow, 0.0, self._bufsize)
        self.y = np.zeros(self._bufsize, dtype=np.float)
        self.y2 = np.zeros(self._bufsize, dtype=np.float)
        self.y3 = np.zeros(self._bufsize, dtype=np.float)
        self.y4 = np.zeros(self._bufsize, dtype=np.float)
        self.session = session()    #assign default session
        self.running = False;

        # Init UI
        self.app = QtGui.QApplication(sys.argv)
        QtGui.QMainWindow.__init__(self)
        self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/ekg.ui', self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        # Init Graph Element
        self.plot = self.ui.graph.getPlotItem()
        self.view = self.plot.getViewBox()
        self.view.setRange(None, (-9,-1), (0.2,adc.voltage()-0.2), None, True, True)
        self.ui.graph.showGrid(x=True, y=True)
        self.ui.graph.setLabel('left', 'amplitude', 'V')
        self.ui.graph.setLabel('bottom', 'time', 's')
        self.curve = self.graph.plot(self.x, self.y, pen=(255,0,0))
        self.curve2 = self.graph.plot(self.x, self.y2, pen=(11,229,245))
        self.curve3 = self.graph.plot(self.x, self.y3, pen=(26,230,39))

        # Filter Setup
        hpass = .05     #highpass frquency in Hz
        lpass = 120     #lowpass frequency in Hz
        bp_bw = .02     #bandpass attenuation bandwidth in Hz
        notch = 50      #notch frquency in Hz
        notch_bw = 10   #notch bandwidth of attenuation in Hz
        Rp = 1          #maximum passband loss in dB
        As = 60         #minimum stopband attenuation in dB
        # Derived parameters
        nyq = self.samplerate/2.0  #nyquist frequency of signal
        bp_bw /= nyq
        notch_bw /= 2.0 * nyq
        hpass /= nyq
        lpass /= nyq
        notch /= nyq
        # Bandpass (.05Hz - 120Hz)
        self.bpB, self.bpA = iirdesign([hpass, lpass], [hpass-bp_bw, lpass+bp_bw], Rp, As, ftype='ellip')
        # Bandstop (45Hz - 55Hz)
        self.bsB, self.bsA = iirdesign([notch-notch_bw, notch+notch_bw], [notch-(notch_bw/2.0), notch+(notch_bw/2.0)], Rp, As, ftype='ellip')

        # Connect Elements
        self.ui.plotButton.clicked.connect(self.togglePlot)
        self.ui.zoominButton.clicked.connect(self.zoomIn)
        self.ui.zoomoutButton.clicked.connect(self.zoomOut)
        self.ui.optionsButton.clicked.connect(self.newWindow)
        GPIO.add_event_detect(21, GPIO.RISING, callback=self.togglePlot, bouncetime=300)
        GPIO.add_event_detect(20, GPIO.FALLING, callback=self.newWindow, bouncetime=300)
        GPIO.add_event_detect(16, GPIO.FALLING, callback=self.zoomIn, bouncetime=300)
        GPIO.add_event_detect(12, GPIO.FALLING, callback=self.zoomOut, bouncetime=300)

        # Show UI
        self.ui.showMaximized()

    def newWindow(self, channel):
        self.options = SolUI.SolBeatMain()

    def zoomIn(self, channel):
        self.view.scaleBy(0.5)

    def zoomOut(self, channel):
        self.view.scaleBy(2.0)

    def togglePlot(self, channel):
        if(self.running):
            self.running = False
            self.ui.plotButton.setText("Start")
        else:
            self.running = True
            self.ui.plotButton.setText("Stop")
            self.getData()

    def getData(self):
        t = time.time()
        bsz = bsz2 = bsz3 = lfilter_zi(self.bsB, self.bsA)

        while (self.running):
            t += self.period
            val, val2, val3 = methods.sample()
            # Filter values - cascade bandstop with bandpass
            val, bsz = lfilter(self.bsB, self.bsA, lfilter(self.bpB, self.bpA, [val]), zi=bsz)
            val2, bsz2 = lfilter(self.bsB, self.bsA, lfilter(self.bpB, self.bpA, [val2]), zi=bsz2)
            val3, bsz3 = lfilter(self.bsB, self.bsA, lfilter(self.bpB, self.bpA, [val3]), zi=bsz3)
            self.buffer.append(val + 2.5)
            self.buffer2.append(val2 + 5)
            self.buffer3.append(val3 + 7.5)
            #SESSION RECORDING
            if(self.session.recording):
                self.session.data.append(val)
            self.y[:] = self.buffer
            self.y2[:] = self.buffer2
            self.y3[:] = self.buffer3
            self.curve.setData(self.x, self.y)
            self.curve2.setData(self.x, self.y2)
            self.curve3.setData(self.x, self.y3)
            self.app.processEvents()
            time.sleep(max(0, t-time.time()))

    def save(self):
        self.session.save()

    def load(self):
        self.session.load()
        time = np.linspace(-(float(self.session.data.size)/self._bufsize)*10, 0.0, self.session.data.size)
        self.curve.setData(time, self.session.data)
        self.app.processEvents()

    def closeEvent(self, event):
        self.running = False
        self.close


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
    def new(self, patient, timestamp = datetime.now(), record = True):
        self.patient = patient
        self.timestamp = timestamp
        self.recording = record

    def save(self):
        methods.save_ses(self.patient, self.timestamp, np.array(self.data))

    def load(self):
        self.data = methods.load_ses(self.patient, self.timestamp)
