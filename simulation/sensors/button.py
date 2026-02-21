import RPi.GPIO as GPIO
import time

def run_button_loop(pin, callback, stop_event, settings):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def gpio_callback(channel):
        value = GPIO.input(pin)
        pressed = (value == GPIO.LOW)

        if pressed:
            callback(True, settings, None)

    GPIO.add_event_detect(
        pin,
        GPIO.FALLING,
        callback=gpio_callback,
        bouncetime=200
    )

    try:
        while not stop_event.is_set():
            time.sleep(0.1)
    finally:
        GPIO.cleanup(pin)