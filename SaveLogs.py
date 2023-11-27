import datetime
import EditConfig
import os


def write(data, name=None):

    savePath = EditConfig.getData().get('save-location') + '/'


    if name is None:
        name = 'log_from_' + str(datetime.datetime.now())

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    file_number = 0
    if os.path.isfile(name):
        while not os.path.isfile(name + str(file_number)):
            file_number += 1

    file_number = str(file_number)

    if file_number == "0":
        logFile = open(savePath + name, 'x')
    else:
        logFile = open(savePath + name + file_number, 'x')

    logFile.write(data)
