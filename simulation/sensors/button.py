import RPi.GPIO as GPIO
import time


def run_button_loop(pin, callback, stop_event, publish_event, settings):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def gpio_callback(channel):
        value = GPIO.input(pin)
        pressed = (value == GPIO.LOW)

        if pressed:
            callback(1, settings, publish_event)
        else:
            callback(0, settings, publish_event)

    GPIO.add_event_detect(
        pin,
        GPIO.BOTH,
        callback=gpio_callback,
        bouncetime=200
    )

    try:
        while not stop_event.is_set():
            time.sleep(0.1)
    finally:
        GPIO.remove_event_detect(pin)
        GPIO.cleanup(pin)