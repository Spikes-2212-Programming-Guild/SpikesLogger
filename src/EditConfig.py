import json


def applyChanges(ip, save_location, logger_nt_location, temp_value):
    conf_data = {
        "logger-nt-location": logger_nt_location,
        "save-location": save_location,
        "serverip": ip,
        "temp-value": temp_value
    }
    with open('../SpikesLog.conf', 'w') as file:
        json.dump(conf_data, file)
    print('config file saved')


def getData():
    try:
        with open('../SpikesLog.conf', 'r') as json_file:
            conf_data = json.load(json_file)
    except:
        conf_data = {
            "logger-nt-location": "SpikesLogger/output",
            "save-location": "logs",
            "serverip": "255.255.255.255",
            "temp-value": "SeaOttersAreSoFuckingCuteINeedThemInMyRoomRightNow" # Thanks to Mr Borito our beloved alumn/mentor who went to FIRST service year
        }
    return conf_data
