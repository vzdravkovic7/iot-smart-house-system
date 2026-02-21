import RPi.GPIO as GPIO

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


class RGBLed:
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red = red_pin
        self.green = green_pin
        self.blue = blue_pin

        GPIO.setup(self.red, GPIO.OUT)
        GPIO.setup(self.green, GPIO.OUT)
        GPIO.setup(self.blue, GPIO.OUT)

        self.turn_off()

    def turn_off(self):
        GPIO.output(self.red, GPIO.LOW)
        GPIO.output(self.green, GPIO.LOW)
        GPIO.output(self.blue, GPIO.LOW)

    def white(self):
        GPIO.output(self.red, GPIO.HIGH)
        GPIO.output(self.green, GPIO.HIGH)
        GPIO.output(self.blue, GPIO.HIGH)

    def red_light(self):
        GPIO.output(self.red, GPIO.HIGH)
        GPIO.output(self.green, GPIO.LOW)
        GPIO.output(self.blue, GPIO.LOW)

    def green_light(self):
        GPIO.output(self.red, GPIO.LOW)
        GPIO.output(self.green, GPIO.HIGH)
        GPIO.output(self.blue, GPIO.LOW)

    def blue_light(self):
        GPIO.output(self.red, GPIO.LOW)
        GPIO.output(self.green, GPIO.LOW)
        GPIO.output(self.blue, GPIO.HIGH)


def rgb_run(mode, settings):
    led = RGBLed(
        settings["red_pin"],
        settings["green_pin"],
        settings["blue_pin"]
    )

    try:
        if mode == 0:
            led.turn_off()
        elif mode == 1:
            led.white()
        elif mode == 2:
            led.red_light()
        elif mode == 3:
            led.green_light()
        elif mode == 4:
            led.blue_light()
    except Exception as e:
        print("RGB error:", e)