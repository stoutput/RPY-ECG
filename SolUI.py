#!/usr/bin/env python

import sys
import os
import re
import string
from PyQt4 import QtCore, QtGui, uic

##Main Window##
class SolBeatMain(QtGui.QMainWindow):
	def __init__(self, parent=None):

		#variables
		
		#initialize and load main UI
        	QtGui.QWidget.__init__(self, parent)
        	#self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/uiDev/main.ui', self)
		#self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/uiDev/optionsmenu.ui', self)
		#self.center() 
		#myPixmap = QtGui.QPixmap('ekgui/uiDev/logo.png')
		#self.pic.setPixmap(myPixmap)
		#self.ui.pic.setScaledContents(True)

     		myapp = optionsMenu()
		myapp.show()

        	#connect buttons 
		#self.ui.exitButton.clicked.connect(self.quit)
		#self.ui.optionsButton.clicked.connect(self.optionsOpen)

	#center the window on the screen
    	def center(self):
        	qr = self.frameGeometry()
        	cp = QtGui.QDesktopWidget().availableGeometry().center()
        	qr.moveCenter(cp)
        	self.move(qr.topLeft())

	#open the options menu
	def optionsOpen(self):
		myapp = optionsMenu()
		myapp.show()

	#close the window
	def quit(self):
		self.close()

##Options Menu##
class optionsMenu(SolBeatMain):
	def __init__(self, parent=None):

		#variables
	
		#initialize and load main UI
		QtGui.QWidget.__init__(self, parent)
		self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/uiDev/optionsmenu.ui', self)
		self.center()


		#connect buttons 
		self.ui.exitButton.clicked.connect(self.back)
		self.ui.selectButton.clicked.connect(self.next)

	def next(self):
		if(self.ui.optionsList.currentRow() == 0):
			self.close()
			myapp = newOrExisting()
			myapp.show()


	def back(self):
		self.close()
		myapp = SolBeatMain()
		myapp.setFocus()

##Patient Prompt##
class newOrExisting(SolBeatMain):
	def __init__(self, parent=None):

		#variables
	
		#initialize and load main UI
		QtGui.QWidget.__init__(self, parent)
		self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/uiDev/neworexist.ui', self)
		self.center()


		#connect buttons 
		self.ui.exitButton.clicked.connect(self.back)
		self.ui.selectButton.clicked.connect(self.next)

	def next(self):
		if(self.ui.listWidget.currentRow() == 0):
			self.close()
			myapp = newUser()
			myapp.show()
		if(self.ui.listWidget.currentRow() == 1):
			self.close()
			myapp = browseusers()
			myapp.show()

	def back(self):
		self.close()
		myapp = optionsMenu()
		myapp.show()

##Create a New User##
class newUser(SolBeatMain):
	def __init__(self, parent=None):

		#variables
	
		#initialize and load main UI
		QtGui.QWidget.__init__(self, parent)
		self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/uiDev/newuser.ui', self)
		self.patientName.setPlaceholderText("First Last") 
		#self.patientNotes.setPlaceholderText("Enter patient notes here.") 
		self.center()


		#connect buttons 
		self.ui.exitButton.clicked.connect(self.back)
		self.ui.selectButton.clicked.connect(self.next)

	
	def next(self):
		#make a patient info directory if there isn't one already
		newpath = os.path.dirname(os.path.abspath(__file__)) + '/patientInfo' 
		if not os.path.exists(newpath):
    			os.makedirs(newpath)
		#create a new folder for the user
		foldername = re.sub('[\W_]+', '', str(self.ui.patientName.text()))
		newpath = os.path.dirname(os.path.abspath(__file__)) + '/patientInfo/' + foldername
		if not os.path.exists(newpath):
    			os.makedirs(newpath)
			#create a patient info file for the entered patient
			filename = foldername
			fd = os.open(newpath + '/' + filename + '.txt', os.O_RDWR|os.O_CREAT|os.O_EXCL)
			with open('patientInfo/patientlist.txt', 'a') as file:
				file.write(str(self.ui.patientName.text()) + '\n')
				file.close
				
			#write info to the file
			ret = os.write(fd, "Patient Name: " + str(self.ui.patientName.text()) + '\n\n' + "---Patient Notes---" + '\n' + str(self.ui.patientNotes.toPlainText()))		
			
			#close the file
			os.close(fd)
			#close the window
			self.close()
			myapp =	genericMessage(str(self.ui.patientName.text()) + " has been added successfully!")
			myapp.show()

		else:
			myapp = genericMessage("No patient entered or patient already exists in database!")
			myapp.show()
			
		
	def back(self):
		self.close()
		myapp = newOrExisting()
		myapp.show()


##Show a List of Existing Users##
class browseusers(SolBeatMain):
	def __init__(self, parent=None):

		#initialize and load main UI
		QtGui.QWidget.__init__(self, parent)
		self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/uiDev/browseusers.ui', self)
		self.center()
		
		#open patientlist file and read from it#
		newpath = os.path.dirname(os.path.abspath(__file__)) + '/patientInfo' 
		if not os.path.exists(newpath):
    			os.makedirs(newpath)
		try:
			with open('patientInfo/patientlist.txt', 'a+') as f:
		    		for line in f:
					line = line.replace('\n', '')
					name = self.lastFirst(line)
					self.ui.userList.addItem(name)

			self.ui.userList.sortItems()

		except 	AttributeError:
			myapp = genericMessage('There are currently no users in the system.')
			myapp.show()
			
			
			
		
		#myapp = genericMessage('There are currently no users in the system.')
		#myapp.show()

		self.ui.selectButton.clicked.connect(self.next)			
		self.ui.exitButton.clicked.connect(self.back)
					#print(line)


		#connect buttons 
		#self.ui.selectButton.clicked.connect(self.next)
	
	def next(self):
		self.close()
		myapp = viewPatientInfo(self.ui.userList.currentItem().text())
		myapp.show()
	
	def back(self):
		self.close()
		myapp = newOrExisting()
		myapp.show()

	def lastFirst(self, name):
		name = ', '.join(reversed(name.split(' ')))
		#print(name)
		return name

##View Selected Patient Information##
class viewPatientInfo(SolBeatMain):
	def __init__(self, name, parent=None):

	#variables

		#initialize and load main UI
		QtGui.QWidget.__init__(self, parent)
		self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/uiDev/viewpatientinfo.ui', self)

		#display patient name
		self.ui.patientName.setText(self.firstLast(name))
		
		#view patient information

				
				
		#read info from the file
		foldername = re.sub('[\W_]+', '', str(self.firstLast(name)))
		newpath = os.path.dirname(os.path.abspath(__file__)) + '/patientInfo' 
		fd = os.open(newpath + '/' + foldername + '/' + foldername + '.txt', os.O_RDWR)
		line = 	os.read(fd, 10000)
		print line
		file.close		
		
		#close the file
		os.close(fd)

		#window stuff

		
	
		self.center()


		#connect buttons 
		self.ui.selectButton.clicked.connect(self.next)
		self.ui.exitButton.clicked.connect(self.back)
	
	def next(self):
		self.close()

	def back(self):
		self.close()
		myapp = browseusers()
		myapp.show()
		
	def firstLast(self, name):
		name = ' '.join(reversed(str(name).split(',')))
		#print(name)
		return name

##Message Popup Template##
class genericMessage(SolBeatMain):
	def __init__(self, message, parent=None):
		#variables

		#initialize and load main UI
		QtGui.QWidget.__init__(self, parent)
		self.ui = uic.loadUi(os.path.dirname(os.path.abspath(__file__)) + '/ekgui/uiDev/genericmessage.ui', self)
		#print out the message
		self.ui.messageBox.setText(message)
	
		self.center()


		#connect buttons 
		self.ui.selectButton.clicked.connect(self.next)
	
	def next(self):
		self.close()


############################################################### 
 

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = SolBeatMain()
	myapp.show()
	sys.exit(app.exec_())
