import sys
import classes
#import spidev

if __name__ == "__main__":
    #spi = spidev.SpiDev()
    #spi.open(0, 0)
    gui = classes.ekgui()
    #spi.close()
    sys.exit(gui.app.exec_())
