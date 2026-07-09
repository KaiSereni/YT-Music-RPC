from http.server import BaseHTTPRequestHandler, HTTPServer
import json, time, threading
from pypresence import Presence
from pypresence.types import ActivityType
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SONG_COVER_URL = "https://yt3.googleusercontent.com/7a03Ybk8vbe8c4dl4E8l77Y4e9aEWjQvTfOAdLdXxsnjZ57gYQ8FsKra9SgXAHT-jtiwuq6lukCfbRKL=w544-h544-l90-rj"
CLIENT_ID = os.getenv("CLIENT_ID")

RETRY_INTERVAL = 5  # Seconds between Discord connection attempts

rpc = None
rpc_lock = threading.Lock()


def connect_rpc():
    """Attempt to connect to Discord RPC, retrying forever until successful."""
    global rpc
    while True:
        try:
            new_rpc = Presence(CLIENT_ID)
            new_rpc.connect()
            with rpc_lock:
                rpc = new_rpc
            print("Connected to Discord RPC.")
            return
        except Exception as e:
            print(f"Discord not available, retrying in {RETRY_INTERVAL}s... ({e})")
            time.sleep(RETRY_INTERVAL)


def rpc_watchdog():
    """Background thread that reconnects to Discord if the connection drops."""
    while True:
        time.sleep(RETRY_INTERVAL)
        with rpc_lock:
            current_rpc = rpc
        if current_rpc is None:
            connect_rpc()


class YTMHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        global rpc
        data = json.loads(self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8'))
        print(data)

        with rpc_lock:
            current_rpc = rpc

        if current_rpc is None:
            print("Discord RPC not connected, skipping update.")
        else:
            try:
                progress = int(data.get('progress', 0)) if data.get('progress') else 0
                current_rpc.update(
                    state=data.get('artist', '').strip(),
                    details=data.get('title', ''),
                    start=int(time.time()) - progress,  # Syncs Discord's progress bar
                    end=int(time.time()) + (int(data['total']) - int(data['progress'])),
                    large_image=data.get('img', DEFAULT_SONG_COVER_URL),
                    large_text="YouTube Music",
                    activity_type=ActivityType.LISTENING
                )
            except Exception as e:
                print(f"Error updating presence (connection may have dropped): {e}")
                with rpc_lock:
                    rpc = None
                # Kick off reconnection in the background
                threading.Thread(target=connect_rpc, daemon=True).start()

        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress default HTTP request logging to keep output clean
        pass


# Initial connection attempt (non-blocking — server starts either way)
threading.Thread(target=connect_rpc, daemon=True).start()

# Watchdog thread to detect and recover from dropped connections
threading.Thread(target=rpc_watchdog, daemon=True).start()

print("Starting HTTP server on localhost:3232...")
HTTPServer(('localhost', 3232), YTMHandler).serve_forever()