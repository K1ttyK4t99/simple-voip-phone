import requests
import os
from dotenv import load_dotenv

load_dotenv()


# ARI credentials and config
ARI_USERNAME = os.getenv("ARI_USERNAME")
ARI_PASSWORD = os.getenv("ARI_PASSWORD")
ARI_URL = os.getenv("ARI_URL")
APP_NAME = os.getenv("APP_NAME")

# Your Telnyx caller ID
CALLER_ID = os.getenv("CALLER_ID")

def originate_call(phone_number):
    # Do NOT strip the '+'
    endpoint = f"PJSIP/{phone_number}@telnyx"

    params = {
        "endpoint": endpoint,
        "extension": "s",
        "app": APP_NAME,
        "callerId": CALLER_ID
    }

    print(f"[*] Attempting to call {phone_number} via endpoint: {endpoint}")

    response = requests.post(f"{ARI_URL}/ari/channels", params=params, auth=(ARI_USERNAME, ARI_PASSWORD))

    if response.status_code == 200:
        print("[+] Call successfully originated.")
    else:
        print(f"[!] Failed to originate call. Status: {response.status_code}")
        print(f"    Response: {response.text}")

if __name__ == "__main__":
    number_to_call = input("Enter the destination phone number (e.g. +15551234567): ").strip()

    if number_to_call.startswith("+") and number_to_call[1:].isdigit():
        originate_call(number_to_call)
    else:
        print("[!] Invalid number format. Use E.164 format (e.g. +15551234567).")

