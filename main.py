# main.py

import subprocess
import time
import call

listener_process = None  # Define early

if __name__ == "__main__":
    try:
        # Prompt FIRST, before starting listener
        number_to_call = input("Enter the destination phone number (e.g. +15551234567): ").strip()

        if number_to_call.startswith("+") and number_to_call[1:].isdigit():
            call.originate_call(number_to_call)
        else:
            print("[!] Invalid number format. Use E.164 format (e.g. +15551234567).")
            exit(1)

        # Now start the listener — after input completes
        listener_process = subprocess.Popen(["python3", "listener.py"])
        print("[*] Listener is running in background. Press Ctrl+C to stop.")

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[!] Shutting down.")
        if listener_process is not None:
            listener_process.terminate()
            listener_process.wait()
