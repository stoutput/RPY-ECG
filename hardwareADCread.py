#Reads and outputs values from the ADC
#Based on scruss.com/blog/2013/02/02/simple-adc-with-the-raspberry-pi

import spidev
import time
import sys

spi = spidev.SpiDev()
spi.open(0, 0)

# read a value from the adc
def readadc(adcnum):
    # if the channel requested is not a valid channel, return an error
    if adcnum > 7 or adcnum < 0:
        return -1
    # otherwise, perform an SPI transaction
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    adcout = ((r[1] & 3) << 8) + r[2]
    volts = (adcout * 3.3) / 1024
    
    return volts

# get a converted value from the ADC
#def getVal():
    #value = readadc(0)
    #volts = (value * 3.3) / 1024
    #print "Voltage:", round(volts,2)
    

#main
if __name__ == '__main__':
    try:
        while True:
            readadc(0)
    #time.sleep(0.5)
    except KeyboardInterrupt:
        spi.close() 
        sys.exit(0)
