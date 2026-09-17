# 20-20-20
A simple timer for the 20-20-20 rule. It has two phases: a 20 minute work period (for looking at your computer), and a 20 second eye rest period where you should focus on something >20 metres away. This helps to reduce myopic development (especially when your degree revolves around computers 😅). Uses Tkinter and pystray.

 - Auto mode toggle sets timer to run continue to next phase without user input
 - Tray icon shows progress through the phase
 - Window can be closed completely to leave the app running in the tray, removing clutter from your desktop while you are working/studying (locks auto mode on).
 - Notification sound lets you know when its time for a break



## Installation

<a name="note"></a>**Note**: since tkinter must run on the main thread, the tray icon does not work on macOS due to lack of support from pystray. Remove `pystray` from `requirements.txt`.


### 1. Download the binary from the releases tab
This will only work on Windows


### 2. Run from source
``` 
git clone github.com/dmkesson/20-20-20
cd 20-20-20
python -m venv .venv
.venv\scripts\activate
pip install -r requirements.txt
python TimerApp.py
```

On macOS/Linux use `source .venv/bin/activate` instead of the 4th line. Also see the [above](#note) note.


### 3. Package from source
Follow the steps in option **2.**, apart from the last line, then:
```
pyinstaller --onefile --windowed --name "20-20-20" --icon=images/icon.ico --add-data "sounds;sounds" --add-data "images;images" TimerApp.py```