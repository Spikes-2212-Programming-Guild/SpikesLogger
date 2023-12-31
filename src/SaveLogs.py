import datetime
import EditConfig
import os


def write(data, name=None):

    save_path = EditConfig.getData().get('save-location') + '/'

    if name is None:
        name = 'log_from_' + str(datetime.datetime.now())

        # Windows is stupid, and cannot deal with a formatted time in a file name so I have to change it for the windows losers
        # BTW, when trying to save a file with ":" in the name you will not get an error, you will get this stupid exit code:
        # Process finished with exit code -1073740791 (0xC0000409)
        name = name.replace(":", "-")

    if not os.path.exists(save_path):
        os.makedirs(save_path)

    file_number = 0

    while os.path.isfile(name + "(" + str(file_number) + ")"):
        file_number += 1

    file_number = str(file_number)

    if file_number == "0":
        log_file = open(save_path + name, 'w')
    else:
        log_file = open(save_path + name + "(" + file_number + ")", 'w')

    log_file.write(data)
    log_file.close()
