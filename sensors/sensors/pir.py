import RPi.GPIO as GPIO

PIR_PIN = 4

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)

def motion_detected(channel):
    print("You moved")
def no_motion(channel):
    print("You stopped moving")

GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=motion_detected)
GPIO.add_event_detect(PIR_PIN, GPIO.FALLING, callback=no_motion)

input("Press any key to exit...")