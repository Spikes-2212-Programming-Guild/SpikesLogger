import datetime
import EditConfig
import os

def write(data, name=None):

    savePath = EditConfig.getData().get('save-location') + '/'

    if name is None:
        name = 'log_from_' + str(datetime.datetime.now())

    if not os.path.exists(savePath):
        os.makedirs(savePath)

    logFile = open(savePath + name, 'w')
    logFile.write(data)
