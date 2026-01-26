import time
import random

def run_ultrasonic_simulator(delay, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        distance = random.uniform(10.0, 150.0)
        callback(distance, settings, publish_event)
        time.sleep(delay)