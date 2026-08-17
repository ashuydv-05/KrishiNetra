import Jetson.GPIO as GPIO
import time
import subprocess
import os
import signal
import sys

# -------- CONFIG --------
BUTTON_PIN = 18 # BOARD pin
SCRIPT_PATH = "/home/tanay/final_7pm/run_parallel.sh"
LOCK_FILE = "/tmp/model_running.lock"
# ------------------------

process = None


def cleanup():
    print("Cleaning up GPIO and exiting...")
    GPIO.cleanup()

    if process:
        try:
            process.terminate()
        except:
            pass

    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)

    sys.exit(0)


# Handle system signals
signal.signal(signal.SIGINT, lambda sig, frame: cleanup())
signal.signal(signal.SIGTERM, lambda sig, frame: cleanup())


def run_script(channel):
    global process

    # Prevent duplicate runs
    if process is not None or os.path.exists(LOCK_FILE):
        print("Already running, ignoring press")
        return

    print("Button pressed → Starting models")

    open(LOCK_FILE, "w").close()

    try:
        process = subprocess.Popen(
            ["/bin/bash", SCRIPT_PATH]
        )

    except Exception as e:
        print(f"Error starting script: {e}")
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
        process = None


def monitor_process():
    global process

    if process is not None:
        ret = process.poll()
        if ret is not None:
            print("Execution finished")
            process = None
            if os.path.exists(LOCK_FILE):
                os.remove(LOCK_FILE)


# -------- SETUP --------
GPIO.setmode(GPIO.BOARD)
GPIO.setup(BUTTON_PIN, GPIO.IN) # no pull_up_down

# Detect button press (LOW -> HIGH if pull-down used)
GPIO.add_event_detect(
    BUTTON_PIN,
    GPIO.RISING,
    callback=run_script,
    bouncetime=300
)

print("GPIO Listener Started. Waiting for button press...")

# -------- MAIN LOOP --------
try:
    while True:
        monitor_process()
        time.sleep(0.2)

except Exception as e:
    print(f"Unexpected error: {e}")
    cleanup()
