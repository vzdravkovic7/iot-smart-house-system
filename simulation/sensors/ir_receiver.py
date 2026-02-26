import RPi.GPIO as GPIO
from datetime import datetime
import time

class IR:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)

        self.buttons = [
            0x300ff22dd,
            0x300ffc23d,
            0x300ff629d,
            0x300ffa857,
            0x300ff9867
        ]

    def get_binary(self):
        num1s = 0
        binary = 1
        command = []
        previousValue = 0
        value = GPIO.input(self.pin)

        while value:
            time.sleep(0.0001)
            value = GPIO.input(self.pin)

        startTime = datetime.now()

        while True:
            if previousValue != value:
                now = datetime.now()
                pulseTime = now - startTime
                startTime = now
                command.append((previousValue, pulseTime.microseconds))

            if value:
                num1s += 1
            else:
                num1s = 0

            if num1s > 10000:
                break

            previousValue = value
            value = GPIO.input(self.pin)

        for (typ, tme) in command:
            if typ == 1:
                if tme > 1000:
                    binary = binary * 10 + 1
                else:
                    binary *= 10

        if len(str(binary)) > 34:
            binary = int(str(binary)[:34])

        return binary

    def read_code(self):
        binary = self.get_binary()
        try:
            value = int(str(binary), 2)
            hex_value = hex(value)
        except:
            return None

        for i, button in enumerate(self.buttons):
            if hex(button) == hex_value:
                return i

        return None


def run_ir_loop(ir, delay, callback, stop_event, publish_event, settings):
    try:
        while not stop_event.is_set():
            code = ir.read_code()
            if code is not None:
                callback(code, publish_event, settings)
            time.sleep(delay)
    finally:
        GPIO.cleanup(ir.pin)