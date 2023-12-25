# SpikesLogger
## Warning!
### python sucks, do not use python at home.
## build command:
### for linux:
```commandline
 pyinstaller --onefile --add-data "SpikesLoggerSmallLogo.png:." SpikesLogger.py
```
### for windows and mac:
```commandline
 pyinstaller --onefile --windowed --add-data "SpikesLoggerSmallLogo.png:." SpikesLogger.py
```

## convert the .ui files to Python
```commandline
pyuic6 LoggerGUI.ui -o LoggerGUI.py
```

## created using pain and FOSS
