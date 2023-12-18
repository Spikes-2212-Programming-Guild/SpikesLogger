import atexit
import os
import sys

from PyQt6.QtGui import QIcon
from networktables import NetworkTables
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QFileDialog
import EditConfig
import LoggerGUI
import SaveLogs
from PIL import Image

# image1 = Image.open(resource_path("SpikesLoggerSmallLogo.png"))
# print(image1.size)
# print('ha')

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
    currentLog += '\n' + value
    gui.updateGUI(currentLog)



sd = NetworkTables.getTable(NTdir)


def startLogging():
    loadConfData()
    NetworkTables.initialize(server=ip)
    #NetworkTables.initialize(server=ip)
    sd.addEntryListener(key=NTvalue, listener=valueChanged)
    print('started')


def pauseLogging():
    sd.removeEntryListener(listener=valueChanged)
    print('paused')


def stopAndSave():
    global currentLog
    pauseLogging()
    if currentLog != "":
        SaveLogs.write(currentLog)
        currentLog = ""
        print('saved')


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

        # self.actionCreate_new_log.triggered.connect(self.wtFile)
        self.ChooseDirPushButton.clicked.connect(self.wtFile)

        self.setWindowIcon(QIcon(resource_path("SpikesLoggerSmallLogo.png")))

        gui = self

    def applyChanges(self):
        EditConfig.applyChanges(self.ServerIP.text(), self.ChooseDirPushButton.text(), self.networkTablesLoggerLocation.text(), self.TempValue.text())

    def updateGUI(self, log):
        self.logsConsole.setText(log)

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


if __name__ == '__main__':
    runGUI()

atexit.register(stopAndSave)
