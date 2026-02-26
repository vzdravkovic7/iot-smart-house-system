import RPi.GPIO as GPIO
import time


class Ultrasonic:
    def __init__(self, trigger_pin, echo_pin):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)


    def get_distance(self):
        GPIO.output(self.trigger_pin, False)
        time.sleep(0.05)

        GPIO.output(self.trigger_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, False)

        pulse_start_time = time.time()
        pulse_end_time = time.time()

        timeout = time.time() + 0.04

        while GPIO.input(self.echo_pin) == 0:
            pulse_start_time = time.time()
            if time.time() > timeout:
                return None

        while GPIO.input(self.echo_pin) == 1:
            pulse_end_time = time.time()
            if time.time() > timeout:
                return None

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300) / 2

        return round(distance, 2)


def run_ultrasonic_loop(ultrasonic, delay, callback, stop_event, publish_event, settings):
    try:
        while not stop_event.is_set():
            distance = ultrasonic.get_distance()

            if distance is not None:
                callback(distance, settings, publish_event)

            time.sleep(delay)
    finally:
        GPIO.cleanup([ultrasonic.trigger_pin, ultrasonic.echo_pin])