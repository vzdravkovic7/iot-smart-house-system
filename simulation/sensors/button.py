# import RPi.GPIO as GPIO
# import time

# class Button(object):
#     BUTTON_OK = 0
#     BUTTON_ERROR = -1
    
#     def __init__(self, pin):
#         self.pin = pin
#         self.state = False
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
#     def readButton(self):
#         try:
#             self.state = not GPIO.input(self.pin)
#             return self.BUTTON_OK
#         except Exception as e:
#             print(f"Error reading button: {e}")
#             return self.BUTTON_ERROR
    
#     def cleanup(self):
#         GPIO.cleanup(self.pin)

# def parseButtonCheckCode(code):
#     if code == 0:
#         return "BUTTON_OK"
#     elif code == -1:
#         return "BUTTON_ERROR"

# def run_button_loop(button, delay, callback, stop_event):
#     while True:
#         check = button.readButton()
#         code = parseButtonCheckCode(check)
#         pressed = button.state
#         callback(pressed, code)
#         if stop_event.is_set():
#             break
#         time.sleep(delay)
