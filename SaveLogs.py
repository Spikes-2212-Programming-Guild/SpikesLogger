import datetime
import EditConfig

def write(data, name=None):

    if name is None:
        name = 'log_from_' + str(datetime.datetime.now())
    logFile = open(EditConfig.getData().get('save-location') + '/' + name, 'w')
    logFile.write(data)
