# Dependencies
import os
import numpy as np
import h5py
from datetime import datetime

# Debugging Dependencies
#import time
#import math
#import random

# Dependent Scripts
import adc


def sample():
    # Debugging
    #value = math.sin(time.time()*60*2*math.pi)
    #value2 = math.sin(time.time()*120*2*math.pi) * math.sin(time.time()*10*2*math.pi)
    #value3 = math.sin(time.time()*70*2*math.pi)
    # Slower, but timing more in-sync
    #value = (adc.readadc(6) - adc.readadc(2))
    #value2 = (adc.readadc(0) - adc.readadc(6))
    #value3 = (adc.readadc(2) - adc.readadc(6))
    adc0 = adc.readadc(0)
    adc2 = adc.readadc(2)
    adc6 = adc.readadc(6)
    value = 2 * (adc2 - adc0)
    value2 = 2 * (adc6 - adc0)
    value3 = 2 * (adc6 - adc2)
    a = (value, value2, value3)
    return a

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
