import spidev
import time
import sys
# SPI Settings


# reference voltage (voltage range)
# changes value across all scripts
refVolt = 4.33

spi = spidev.SpiDev()
spi.open(0, 0)
#spi.max_speed_hz = 200



# read a value from the adc
def readadc(adcnum):

    # error checking - SLOW
    # if the channel requested is not a valid channel, return an error
    #if adcnum > 7 or adcnum < 0:
     #   return -1

    # perform an SPI transaction
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    return ((((r[1] & 3) << 8) + r[2]) * refVolt) / 1024

# return reference voltage of ADC
def voltage():
    return refVolt

# main
if __name__ == '__main__':
    try:
        while True:
            x = readadc(0)
            y = readadc(1)
            print(x, y)
    #time.sleep(0.5)
    except KeyboardInterrupt:
        spi.close() 
        sys.exit(0)
