import time
import random

def run_ir_simulator(delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        code = random.choice([0, 1, 2, 3, 4])
        callback(code, publish_event, settings)
        time.sleep(delay)
