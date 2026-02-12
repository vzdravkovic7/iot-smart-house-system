import random
import time

def run_dht_simulator(interval, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        temperature = round(random.uniform(20, 30), 2)
        humidity = round(random.uniform(40, 60), 2)

        callback(temperature, humidity, settings, publish_event)
        time.sleep(interval)
