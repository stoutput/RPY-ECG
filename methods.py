import os
import time
import math
import random
import numpy as np
import h5py
from datetime import datetime

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
def save_ses(user, time, data):
    path = os.path.dirname(os.path.abspath(__file__)) + '/sessions/'
    if not os.path.exists(path):
        os.mkdir(path)
    session = h5py.File(path + user + '.h5', 'w')
    if session:
        session.create_dataset(time, data=data, compression='gzip', compression_opts=5)
        session.close()
        return True
    else:
        return False

def load_ses(user, time):
    path = os.path.dirname(os.path.abspath(__file__)) + '/sessions/' + user
    session = h5py.File(path + '.h5', 'r')
    if session:
        data = session[time][:]
        session.close()
        return np.array(data)
    else:
        return False

#accepts a plotItem as argument (ekgui.plot)
#saves plot screenshot as png
def save_scr(plot):
    path = os.path.dirname(os.path.abspath(__file__)) + '/screenshots/' + datetime.now()
