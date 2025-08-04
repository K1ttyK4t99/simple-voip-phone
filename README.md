# Telnyx ARI Caller

This project originates a call via Telnyx and handles the ARI WebSocket events to play audio and hang up.

## Requirements

- Python 3.x
- `requests`, `websocket-client`, `python-dotenv`

## Usage

1. Set up an Asterisk PBX and get a number through Telnyx (or other SIP Trunking service)
2. Create a `.env` file with your ARI credentials
3. Run `python main.py`
