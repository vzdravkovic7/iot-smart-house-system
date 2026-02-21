import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Keypad:
    def __init__(self, settings):
        self.rows = settings["rows"]
        self.cols = settings["cols"]

        for row in self.rows:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.LOW)

        for col in self.cols:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        self.keys = [
            ["1","2","3","A"],
            ["4","5","6","B"],
            ["7","8","9","C"],
            ["*","0","#","D"]
        ]

    def read_key(self):
        for i, row in enumerate(self.rows):
            GPIO.output(row, GPIO.HIGH)

            for j, col in enumerate(self.cols):
                if GPIO.input(col) == 1:
                    GPIO.output(row, GPIO.LOW)
                    return self.keys[i][j]

            GPIO.output(row, GPIO.LOW)

        return None


def keypad_run(settings, callback, stop_event):
    keypad = Keypad(settings)
    pin_buffer = ""

    try:
        while not stop_event.is_set():
            key = keypad.read_key()

            if key:
                if key.isdigit():
                    pin_buffer += key
                    print("Pressed:", key)

                if len(pin_buffer) == 4:
                    callback(pin_buffer, settings)
                    pin_buffer = ""

                time.sleep(0.3)  # debounce

            time.sleep(0.05)

    except Exception as e:
        print("Keypad error:", e)