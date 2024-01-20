import atexit
import os
import sys

from PyQt6.QtGui import QIcon
from networktables import NetworkTables
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QApplication, QFileDialog
import webbrowser

import EditConfig
import LoggerGUI
import SaveLogs

conf_data = None
ip = "255.255.255.255"
logger_location = "SpikesLogger/output"
nt_dir = logger_location.rsplit('/')[0]
nt_value = logger_location.rsplit('/')[1]
temp_value = "SeaOttersAreSoFuckingCuteINeedThemInMyRoomRightNow"  # Thanks to Mr Borito our beloved alumn/mentor who went to FIRST service year

gui = None
current_log = ""


# get the data from the config file
def load_conf_data():
    global conf_data, ip, logger_location, nt_dir, nt_value, temp_value

    conf_data = EditConfig.getData()
    ip = str(conf_data.get("serverip"))
    logger_location = str(conf_data.get("logger-nt-location"))
    nt_dir = logger_location.rsplit('/')[0]
    nt_value = logger_location.rsplit('/')[1]
    temp_value = str(conf_data.get("temp-value"))

load_conf_data()

# when value is logged
def value_changed(table, key, value, isNew):
    global current_log
    if value != temp_value:
        print("logged: " + value)
        table.putString(nt_value, temp_value)
        current_log += value + '\n'
        gui.update_gui(current_log)


def start_logging():
    load_conf_data()
    NetworkTables.initialize(server=ip)
    SpikesLogger_table.addEntryListener(key=nt_value, listener=value_changed)
    print('started (ip: ' + ip + " | location: " + nt_dir + "/" + nt_value + ")")
    gui.StatusLabel.setText("<font color='green'>logging</font>")


def pause_logging():
    SpikesLogger_table.removeEntryListener(listener=value_changed)
    print('paused')
    try:
        gui.StatusLabel.setText("<font color='orange'>paused</font>")
    except:
        print('gui is closed hmmmm')


def stop_and_save():
    global current_log, gui
    pause_logging()
    try:
        gui.StatusLabel.setText("<font color='red'>off</font>")
    except:
        print('gui is closed')
    if current_log != "":
        SaveLogs.write(current_log)
        current_log = ""
        print('saved')
        try:
            gui.update_gui("Log file saved, press start to start logging...")
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

        self.StartPushButton.clicked.connect(start_logging)
        self.PausePushButton.clicked.connect(pause_logging)
        self.SaveAndStopPushButton.clicked.connect(stop_and_save)
        self.applyChangesPushButton.clicked.connect(self.apply_changes)

        self.ServerIP.setText(conf_data.get("serverip"))
        self.ChooseDirPushButton.setText(conf_data.get("save-location"))
        self.networkTablesLoggerLocation.setText(conf_data.get("logger-nt-location"))
        self.TempValue.setText(conf_data.get("temp-value"))
        self.ChooseDirPushButton.clicked.connect(self.open_file_dialog)

        self.actionUpdate.triggered.connect(update_app)
        self.actionAbout.triggered.connect(run_about)
        self.actionSource_code.triggered.connect(see_source_code)

        self.setWindowIcon(QIcon(resource_path("SpikesLoggerSmallLogo.png")))

        gui = self

    def apply_changes(self):
        EditConfig.applyChanges(self.ServerIP.text(), self.ChooseDirPushButton.text(), self.networkTablesLoggerLocation.text(), self.TempValue.text())

    def update_gui(self, log):
        self.logsConsole.setText(log)
        self.scrollArea.ensureVisible(0, self.logsConsole.height())

    def open_file_dialog(self):
        save_path = QFileDialog.getExistingDirectoryUrl().path()
        if save_path != "":
            if os.name == "nt":  # the nt Windows kernel
                save_path = save_path.removeprefix("/")
            self.ChooseDirPushButton.setText(save_path)


def run_gui():
    app = QApplication(sys.argv)
    form = SpikesLoggerGUI()
    form.show()
    app.exec()


# Python suckssss!!!11!!!1!!!11
# if you want to, you can create a normal about dialog yourself,
# but use this text tho if you do:
# SpikesLogger is an app developed by The Spikes #2212 used to log values from the robot to the computer in real time.
# the source code is available here under GPLv3 licence.
def run_about():
    webbrowser.open('https://github.com/Spikes-2212-Programming-Guild/SpikesLogger/blob/main/README.md')


def update_app():
    webbrowser.open('https://github.com/Spikes-2212-Programming-Guild/SpikesLogger/releases')


def see_source_code():
    webbrowser.open('https://github.com/Spikes-2212-Programming-Guild/SpikesLogger')


if __name__ == '__main__':
    global SpikesLogger_table
    load_conf_data()
    SpikesLogger_table = NetworkTables.getTable(nt_dir)
    atexit.register(stop_and_save)
    run_gui()
