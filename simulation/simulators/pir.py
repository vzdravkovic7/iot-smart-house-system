import time
import random

def run_pir_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        motion = random.choice([True, False])
        callback(motion)
        time.sleep(delay)