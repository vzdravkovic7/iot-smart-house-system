import time
import random

def run_membrane_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        key = random.choice([None, '1', '2', '3', 'A', 'B'])
        if key:
            callback(key)
        time.sleep(delay)