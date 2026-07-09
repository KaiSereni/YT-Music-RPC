# YouTube Music Discord Presence Script

Tested for MacOS, probably works on any OS

## QuickStart

- Clone the repo.
- On Chrome, Brave, Opera, or any other Chromium-based browser, go to [chrome://extensions](chrome://extensions), enable developer mode in the top right, and click "Load unpacked". Navigate to and select the "extension" folder in this repo.
- Create a Python venv with `python -m venv venv`. Activate the venv with `source venv/bin/activate` on Mac or Linux, or `venv/Scripts/activate` on Windows. Run `pip install -r requirements.txt`.
- Anytime you play music with YT Music in your browser while running both [server.py](./server.py) and the Discord desktop app (the web client won't work) at the same time, your music will display in your status.

## Auto-run on startup (Mac)

- Open the Automator app
- Create a new document, and select "Application".
- Add a Run Shell Script action. If the path to the repo on your computer is `~/Documents/musicpresence/`, the command would be:
```
~/Documents/musicpresence/venv/bin/python ~/Documents/musicpresence/server.py
```
make sure to replace these example paths with the correct path.
- Save the automator application. Go to System Settings > General > Login Items and add the saved application to your login items.
- If you prefer use the Discord web client instead of the app, you can make it run in the background on startup by creating a second startup automator script with the command: 
```
/Applications/Discord.app/Contents/MacOS/Discord --start-minimized
```
No, I did not upload my .env file by accident. Client IDs are public.