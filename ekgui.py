# Dependencies
import sys

#Dependent Scripts
import classes

if __name__ == "__main__":
    gui = classes.ekgui()
    sys.exit(gui.app.exec_())
