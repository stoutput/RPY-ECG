#!/bin/sh

sudo apt-get update
sudo apt-get install python-dev
sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose -y
sudo apt-get install python-pyqtgraph -y
sudo apt-get install libhdf5-dev -y
sudo apt-get install python-pip -y
sudo pip install numpy
sudo pip install h5py
sudo pip install spidev
