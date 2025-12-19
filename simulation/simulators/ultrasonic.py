import time
import random


def run_ultrasonic_simulator(delay, callback, stop_event):
    while not stop_event.is_set():
        distance = random.uniform(10.0, 150.0)
        callback(distance)
        time.sleep(delay)