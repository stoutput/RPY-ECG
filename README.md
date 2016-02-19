#rpy-ecg
#### A Python ECG for the Raspberry Pi


#####FEATURES
---
* 8-channel ADC input over SPI
* Written entirely in Python
* Zoom in/out
* Session saving and loading
* Screenshot save

#####DESCRIPTION
---
* ekgui.py: main script, spawns GUI and threads
* hardwareADCread.py: facilitates reading from ADC through SPI
* /ekgui: contains the GUI (ekgui.ui) and files for editing in Qt Creator

#####DEPENDENCIES
---
* [Pyqtgraph](http://www.pyqtgraph.org/)
* [Spidev](https://pypi.python.org/pypi/spidev)
* [Numpy](http://www.numpy.org/)
