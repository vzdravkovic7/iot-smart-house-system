import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def buzz(self, pitch=440, duration=0.2):
        period = 1.0 / pitch
        delay = period / 2
        cycles = int(duration * pitch)

        for _ in range(cycles):
            GPIO.output(self.pin, True)
            time.sleep(delay)
            GPIO.output(self.pin, False)
            time.sleep(delay)

    def on(self):
        GPIO.output(self.pin, True)

    def off(self):
        GPIO.output(self.pin, False)

    def cleanup(self):
        GPIO.output(self.pin, False)
        GPIO.cleanup(self.pin)

def buzzer_run(action, pin):
    buzzer = Buzzer(pin)

    try:
        if action:
            buzzer.buzz(440, 0.3)
        else:
            buzzer.off()
    except Exception as e:
        print("Buzzer error:", e)