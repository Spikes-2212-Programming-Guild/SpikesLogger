## Warning!
### [python sucks](https://gitlab.com/TzintzeneT/dont-use-python), do not use python at home.

# SpikesLogger
![SpikesLogger screenshot](Screenshot1.png "Awesome app")

Welcome to the SpikesLogger official repo!
this app is the desktop part of the SpikesLogger real-time FRC logger.
The SpikesLogger uses the NetworkTables server on the (holy) roborio to log values from the robot to your computer.

You can download the latest release from [here](https://github.com/Spikes-2212-Programming-Guild/SpikesLogger/releases), or build it yourself with the commands below.
the SpikesLogger is designed to replace the "System.out.println()" you do every time you want to log some value when you run your code.
it is meant to be used for debugging but feel free to use it as you want.

# logging values
1. _FIRST_, set the "server IP" setting in the app to your roborio's ip.
2. _SECOND_, to log the values from your robot, you can use a couple of methods.

**note:** make sure to not log the temp value in the app settings, otherwise it will not be logged.
if for some odd reason you want to log "SeaOttersAreSoFuckingCuteINeedThemInMyRoomRightNow",
you can change it to a different value.

### using SpikesLib2
you can [install SpikesLib2](https://github.com/Spikes-2212-Programming-Guild/SpikesLib2#installation) 
and use the built-in SpikesLogger using 
```
SpikesLogger sl = new SpikesLogger();
sl.log(value);
```


### Putting values in to the NetworkTables
Although not recommended, you can put the values that you want to log at a certain location in the NetworkTables, for example: SpikesLogger/output.
After that, you need to put in the app settings the NetworkTables location at the "Logger Location" and hit apply.
Also **make sure** to not update the value periodically unless you want to log that same value periodically.

this method is not recommended because you can accidentally put the value in the wrong place,
or do other stupid things you won't notice and will drive you insane.


### Creating your own
You can create your own robot logger in your preferred language (Java/C++/Python) to use with this desktop app.
you can take a look at the SpikesLogger class in SpikesLib2 for inspiration or just create one from scratch.
To do that, you'll need to make sure you are putting all of the values at the same location at the NetworkTables,
and you also need to put in the desktop app settings the "Logger Location" as that NetworkTables location.


# build commands:
### for linux:
```commandline
 pyinstaller --onefile --add-data "SpikesLoggerSmallLogo.png:." SpikesLogger.py
```
### for windows and mac:
```commandline
 pyinstaller --onefile --windowed --icon=SpikesLoggerIcon.ico --add-data "SpikesLoggerSmallLogo.png:." SpikesLogger.py
```

## convert the .ui GUI file to Python
```commandline
pyuic6 LoggerGUI.ui -o LoggerGUI.py
```

## created using pain and FOSS
This app is licensed under the awesome GPLv3 licence, and written in Python (unfortunately).