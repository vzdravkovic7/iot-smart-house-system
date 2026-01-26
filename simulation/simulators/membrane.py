import time
import random

def run_membrane_simulator(delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        key = random.choice([None, '1', '2', '3', 'A', 'B'])
        if key:
            callback(key, settings, publish_event)
        time.sleep(delay)