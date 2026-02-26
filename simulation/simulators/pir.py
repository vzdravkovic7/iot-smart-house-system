import time
import random

def run_pir_simulator(delay, callback, stop_event, publish_event, settings, diode_settings):
    while not stop_event.is_set():
        motion = random.choice([True, False])
        callback(motion, settings, publish_event, diode_settings)
        time.sleep(delay)
