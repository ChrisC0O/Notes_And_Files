### Create .exe with PyInstaller:
```ps1
pyinstaller -F .\SCRIPT.py --onefile
```
If using [Alive-Progress](https://pypi.org/project/alive-progress/):
```ps1
pyinstaller -F --collect-data grapheme .\SCRIPT.py --onefile
```
Use --windowed to hide the terminal
```ps1
pyinstaller --onefile --windowed your_script.py
```



### URL encode with urllib:
```py
import urllib.parse

print(urllib.parse.quote("http://www.sample.com/", safe=""))
```


### Get Unix time stamp:
```py
import time

time.time()
```
