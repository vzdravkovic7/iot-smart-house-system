import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class Keypad:
    def __init__(self, settings):
        self.rows = settings["rows"]
        self.cols = settings["cols"]

        # Rows = OUTPUT
        for row in self.rows:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.LOW)

        # Cols = INPUT with PULL-DOWN
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
                    key = self.keys[i][j]

                    # čekaj otpust da ne duplira
                    while GPIO.input(col) == 1:
                        time.sleep(0.01)

                    GPIO.output(row, GPIO.LOW)
                    return key

            GPIO.output(row, GPIO.LOW)

        return None


def keypad_run(settings, callback, stop_event):
    keypad = Keypad(settings)
    pin_buffer = ""

    try:
        while not stop_event.is_set():
            key = keypad.read_key()

            if key:
                print("Pressed:", key)

                if key.isdigit():
                    pin_buffer += key

                # kada stignu 4 cifre
                if len(pin_buffer) == 4:
                    print("PIN entered:", pin_buffer)
                    callback(pin_buffer, settings)
                    pin_buffer = ""

                time.sleep(0.2)  # debounce

            time.sleep(0.05)

    finally:
        GPIO.cleanup()