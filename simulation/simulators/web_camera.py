import time
import random

def run_web_camera_simulator(interval, callback, stop_event, publish_event, settings):
    while not stop_event.is_set():
        motion_detected = random.choice([0, 1])
        callback(motion_detected, settings, publish_event)
        time.sleep(interval)
