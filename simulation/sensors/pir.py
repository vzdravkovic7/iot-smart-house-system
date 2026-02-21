import RPi.GPIO as GPIO
import time


class PIR:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)


def run_pir(pir, delay, callback, stop_event, publish_event, settings, diode_settings):
    def motion_detected(channel):
        callback(True, settings, publish_event, diode_settings)

    def no_motion(channel):
        callback(False, settings, publish_event, diode_settings)

    GPIO.add_event_detect(pir.pin, GPIO.RISING, callback=motion_detected)
    GPIO.add_event_detect(pir.pin, GPIO.FALLING, callback=no_motion)

    try:
        while not stop_event.is_set():
            time.sleep(delay)
    finally:
        GPIO.cleanup(pir.pin)