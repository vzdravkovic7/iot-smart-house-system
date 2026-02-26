import RPi.GPIO as GPIO

class Buzzer:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.pin, GPIO.HIGH)

    def off(self):
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        GPIO.output(self.pin, GPIO.LOW)
        GPIO.cleanup(self.pin)


def buzzer_run(action, pin):
    buzzer = Buzzer(pin)

    try:
        if action:      # ON signal
            buzzer.on()
        else:           # OFF signal
            buzzer.off()
    except Exception as e:
        print("Buzzer error:", e)