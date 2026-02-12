import random
import time

def run_gyro_simulator(interval, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        x = round(random.uniform(-5, 5), 2)
        y = round(random.uniform(-5, 5), 2)
        z = round(random.uniform(-5, 5), 2)

        callback(x, y, z, settings, publish_event)
        time.sleep(interval)
