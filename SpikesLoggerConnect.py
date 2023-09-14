#this file is connecting between the front and back end of the logger
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication
import sys
import os
import LoggerGUI

from networktables import NetworkTables
import datetime
import time
import atexit

gui = None

# the ip of the networktables server (robot)
ip = "10.22.12.2" #None #"10.22.12.2"

# loggerConf = open("logger.conf", "r")
# logNumber = int(loggerConf.read()) + 1 #int(str(loggerConf)) + 
# loggerConf.close()
#print(logNumber)

# storedata
logstr = None # open("log" + str(logNumber) + ".txt", "w")
loglog = ""

# loggerConf = open("logger.conf", "w")
# loggerConf.write(str(logNumber))
# loggerConf.close()

#loggerConf.write(logNumber)
#loggerConf.close()

#table = None

# Function called when value changes
def valueChanged(table, key, value, isNew):
    
    global loglog
    logged = "[" + str(datetime.datetime.now()) + "]: " + str(value)
    #logstr.write(logged + "\n")
    loglog += logged + "\n"
    print(logged)
    gui.logsConsole.setText(logged + "\n" + gui.logsConsole.text())
    #print(gui.logsConsole.text())
    table.putString(gui.networkTablesLoggerLocation.text().rsplit('/', 1)[1], 'SeaOttersAreSoFuckingCuteINeedThemInMyRoomRightNow') #Thanks to Mr Borito our beloved alumn/mentor who went to FIRST service year


table = None


#start the logger
def startLogger():
    # Connect to NetworkTables
    global logstr, logNumber, gui, ip, Networktables, table, loglog
    
    valueServerLocation = gui.networkTablesLoggerLocation.text().rsplit('/', 1)
    ip = str(gui.ServerIP.text())
    # print(ip + " ----- " + gui.ServerIP.text())
    if logstr == None:
        print('new log')
        loggerConf = open("logger.conf", "r")
        logNumber = int(loggerConf.read()) + 1
        loggerConf.close()

        loggerConf = open("logger.conf", "w")
        loggerConf.write(str(logNumber))
        loggerConf.close()

        if not os.path.exists(gui.savedLogsLocation.text()):
            os.makedirs(gui.savedLogsLocation.text())

        logstr = open(gui.savedLogsLocation.text() + "/log" + str(logNumber) + ".txt", "w")

        print(gui.savedLogsLocation.text())

        loglog = ""
        gui.logsConsole.setText("")

    NetworkTables.initialize(server=ip)
    # Get the table you want to listen to 
    table = NetworkTables.getTable(valueServerLocation[0])
    # Add the listener for the logger in the networktables
    table.addEntryListener(key=valueServerLocation[1], listener=valueChanged)
    print(gui.networkTablesLoggerLocation.text())


#stop the logger
def stopLogger():
    try:
        table.removeEntryListener(listener=valueChanged)
    except:
        print('closed already')
    print("stoped")

#stop the logger
def stopAndSave():
    #table.removeEntryListener(listener=valueChanged)
    global loglog, logstr
    stopLogger()
    print("goodbye")
    if logstr is not None:
        logstr.write(loglog)
        logstr.close()
        logstr = None
    

class ExampleApp(QtWidgets.QMainWindow, LoggerGUI.Ui_SpikesLoggerGuiWindow):
    
    def __init__(self, parent=None):
        global gui
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)

        self.StartPushButton.clicked.connect(startLogger)
        self.StopPushButton.clicked.connect(stopLogger)
        self.SaveAndStopPushButton.clicked.connect(stopAndSave)
        self.actionCreate_new_log.triggered.connect(startLogger)
        # self.scrollAreaWidgetContents.scroll()
        
        gui = self

def main():
    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec()


if __name__ == '__main__':
    main()
    print("help me please")



atexit.register(stopAndSave)