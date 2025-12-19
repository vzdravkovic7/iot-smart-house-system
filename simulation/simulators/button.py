import time
import random

def run_button_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        pressed = random.choice([True, False])
        callback(pressed)
        time.sleep(delay)