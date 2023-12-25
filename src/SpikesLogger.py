import atexit
import os
import sys

from PyQt6.QtGui import QIcon
from networktables import NetworkTables
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QFileDialog, QDialog, QLabel
import webbrowser

import EditConfig
import LoggerGUI
import SaveLogs


confData = None
ip = "255.255.255.255"
LoggerLocation = "SpikesLogger/output"
NTdir = LoggerLocation.rsplit('/')[0]
NTvalue = LoggerLocation.rsplit('/')[1]
temp_value = "SeaOttersAreSoFuckingCuteINeedThemInMyRoomRightNow" # Thanks to Mr Borito our beloved alumn/mentor who went to FIRST service year

gui = None
currentLog = ""

# get the data from the config file
def loadConfData():

    global confData, ip, LoggerLocation, NTdir, NTvalue, temp_value

    confData = EditConfig.getData()
    ip = str(confData.get("serverip"))
    LoggerLocation = str(confData.get("logger-nt-location"))
    NTdir = LoggerLocation.rsplit('/')[0]
    NTvalue = LoggerLocation.rsplit('/')[1]
    temp_value = str(confData.get("temp_value"))


loadConfData()
# NetworkTables.initialize(server=ip)


#when value is looged
def valueChanged(table, key, value, isNew):
    global currentLog
    print("logged: " + value)
    table.putString(NTvalue, temp_value)
    currentLog += value + '\n'
    gui.updateGUI(currentLog)



sd = NetworkTables.getTable(NTdir)


def startLogging():
    loadConfData()
    NetworkTables.initialize(server=ip)
    sd.addEntryListener(key=NTvalue, listener=valueChanged)
    print('started')
    gui.StatusLable.setText("<font color='green'>logging</font>")


def pauseLogging():
    sd.removeEntryListener(listener=valueChanged)
    print('paused')
    try:
        gui.StatusLable.setText("<font color='orange'>paused</font>")
    except:
        print('gui is closed')

def stopAndSave():
    global currentLog, gui
    pauseLogging()
    try:
        gui.StatusLable.setText("<font color='red'>off</font>")
    except:
        print('gui is closed')
    if currentLog != "":
        SaveLogs.write(currentLog)
        currentLog = ""
        print('saved')
        try:
            gui.updateGUI("Press start to start logging...")
        except:
            print('gui is closed')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class SpikesLoggerGUI(QtWidgets.QMainWindow, LoggerGUI.Ui_SpikesLoggerGuiWindow):

    def __init__(self, parent=None):
        global gui

        super(SpikesLoggerGUI, self).__init__(parent)
        self.setupUi(self)

        self.StartPushButton.clicked.connect(startLogging)
        self.PausePushButton.clicked.connect(pauseLogging)
        self.SaveAndStopPushButton.clicked.connect(stopAndSave)
        self.applyChangesPushButton.clicked.connect(self.applyChanges)

        self.ServerIP.setText(confData.get("serverip"))
        self.ChooseDirPushButton.setText(confData.get("save-location"))
        self.networkTablesLoggerLocation.setText(confData.get("logger-nt-location"))
        self.TempValue.setText(confData.get("temp-value"))
        self.ChooseDirPushButton.clicked.connect(self.wtFile)

        self.actionUpdate.triggered.connect(self.updateApp)
        self.actionAbout.triggered.connect(run_about)
        self.actionSource_code.triggered.connect(see_source_code)

        self.setWindowIcon(QIcon(resource_path("SpikesLoggerSmallLogo.png")))

        gui = self
        gui.StatusLable

    def applyChanges(self):
        EditConfig.applyChanges(self.ServerIP.text(), self.ChooseDirPushButton.text(), self.networkTablesLoggerLocation.text(), self.TempValue.text())

    def updateApp(self):
        webbrowser.open('https://github.com/Spikes-2212-Programming-Guild/SpikesLogger/releases')

    def updateGUI(self, log):
        self.logsConsole.setText(log)
        self.scrollArea.ensureVisible(0, self.logsConsole.height())

    def wtFile(self):
        save_path = QFileDialog.getExistingDirectoryUrl().path()
        if save_path != "":
            if os.name == "nt":  # the nt Windows kernel
                save_path = save_path.removeprefix("/")
            self.ChooseDirPushButton.setText(save_path)



def runGUI():
    app = QApplication(sys.argv)
    form = SpikesLoggerGUI()
    form.show()
    app.exec()


# Python suckssss!!!11!!!1!!!11
# if you want you can create a normal about dialog yourself
# but use this text tho if you do:
# SpikesLogger is an app developed by TheSpikes#2212 used to log values from the robot to the computer in real time.
# the source code is available here under GPLv3 licence.
def run_about():
    webbrowser.open('https://github.com/Spikes-2212-Programming-Guild/SpikesLogger/blob/main/README.md')


def see_source_code():
    webbrowser.open('https://github.com/Spikes-2212-Programming-Guild/SpikesLogger')


if __name__ == '__main__':
    runGUI()

atexit.register(stopAndSave)
