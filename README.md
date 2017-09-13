# RPY-ECG
### A Python ECG for the Raspberry Pi


##### FEATURES
---
* 8-channel ADC input over SPI
* Written entirely in Python
* Zoom in/out
* Session saving and loading
* Screenshot save
* Patient info

##### DESCRIPTION
---
* `ekgui.py`: main script, spawns GUI and threads
* `hardwareADCread.py`: facilitates reading from ADC through SPI
* `/ekgui`: contains the GUI (ekgui.ui) and files for editing in Qt Creator

##### DEPENDENCIES
---
* [PyQtGraph](http://www.pyqtgraph.org/)
* [Spidev](https://pypi.python.org/pypi/spidev)
* [Numpy](http://www.numpy.org/)
* [H5py](http://www.h5py.org/)
