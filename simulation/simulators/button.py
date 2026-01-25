import time
import random

def run_button_simulator(delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        pressed = random.choice([True, False])
        callback(pressed, settings, publish_event)
        time.sleep(delay)