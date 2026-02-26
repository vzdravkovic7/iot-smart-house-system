import RPi.GPIO as GPIO
import time


class PIR:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)


def run_pir(pir, delay, callback, stop_event, publish_event, settings, diode_settings):

    def motion_callback(channel):
        state = GPIO.input(pir.pin)

        if state == GPIO.HIGH:
            callback(True, settings, publish_event, diode_settings)
        else:
            callback(False, settings, publish_event, diode_settings)

    GPIO.add_event_detect(pir.pin, GPIO.BOTH, callback=motion_callback)

    try:
        while not stop_event.is_set():
            time.sleep(delay)
    finally:
        GPIO.remove_event_detect(pir.pin)
        GPIO.cleanup(pir.pin)