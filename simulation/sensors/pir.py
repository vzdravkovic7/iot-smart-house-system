# import RPi.GPIO as GPIO
# import time

# class PIR(object):
#     PIR_OK = 0
#     PIR_ERROR = -1
    
#     def __init__(self, pin):
#         self.pin = pin
#         self.motion = False
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.pin, GPIO.IN)
    
#     def readPIR(self):
#         try:
#             self.motion = GPIO.input(self.pin)
#             return self.PIR_OK
#         except Exception as e:
#             print(f"Error reading PIR: {e}")
#             return self.PIR_ERROR
    
#     def cleanup(self):
#         GPIO.cleanup(self.pin)

# def parsePIRCheckCode(code):
#     if code == 0:
#         return "PIR_OK"
#     elif code == -1:
#         return "PIR_ERROR"

# def run_pir_loop(pir, delay, callback, stop_event):
#     while True:
#         check = pir.readPIR()
#         code = parsePIRCheckCode(check)
#         motion = pir.motion
#         callback(motion, code)
#         if stop_event.is_set():
#             break
#         time.sleep(delay)
