import requests
import websocket
import threading
import json
import time
import base64
import os
from dotenv import load_dotenv

load_dotenv()

ARI_USERNAME = os.getenv("ARI_USERNAME")
ARI_PASSWORD = os.getenv("ARI_PASSWORD")
ARI_URL = os.getenv("ARI_URL")
APP_NAME = os.getenv("APP_NAME")

def answer_channel(channel_id):
    requests.post(f'{ARI_URL}/ari/channels/{channel_id}/answer',
                  auth=(ARI_USERNAME, ARI_PASSWORD))

def hangup_channel(channel_id):
    requests.delete(f'{ARI_URL}/ari/channels/{channel_id}',
                    auth=(ARI_USERNAME, ARI_PASSWORD))

   
def play_sound(channel_id):
    payload = {
            "media": "sound:hello-world"
    }
    r = requests.post(f'{ARI_URL}/ari/channels/{channel_id}/play',
                    auth=(ARI_USERNAME, ARI_PASSWORD), json=payload)
    print("Playing audio...")

def on_message(ws, message):
    event = json.loads(message)
    if event['type'] == 'StasisStart':
        channel = event['channel']
        channel_id = channel['id']
        print(f"[+] Incoming channel: {channel_id}")

        answer_channel(channel_id)
        print("[*] Call answered")

        play_sound(channel_id)
        time.sleep(3)

        hangup_channel(channel_id)
        print("[*] Call hung up.")

def on_error(ws, error):
    print(f"[!] WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("[*] WebSocket connection closed.")

def on_open(ws):
    print("WebSocket connected. Listening for calls to 'listener'...")

def run_ws():
    credentials = f"{ARI_USERNAME}:{ARI_PASSWORD}"
    b64_credentials = base64.b64encode(credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {b64_credentials}"
    }
    ws_url = f"ws://localhost:8088/ari/events?app={APP_NAME}&subscribeAll=true"
    ws = websocket.WebSocketApp(ws_url,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close,
                                header=headers)
    ws.on_open = on_open
    ws.run_forever()

# Start ARI WebSocket listener
run_ws()
