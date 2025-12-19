# import RPi.GPIO as GPIO
# import time

# class Ultrasonic(object):
#     ULTRASONIC_OK = 0
#     ULTRASONIC_ERROR_TIMEOUT = -1
#     ULTRASONIC_ERROR = -2
    
#     def __init__(self, trigger_pin, echo_pin):
#         self.trigger_pin = trigger_pin
#         self.echo_pin = echo_pin
#         self.distance = 0.0
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(self.trigger_pin, GPIO.OUT)
#         GPIO.setup(self.echo_pin, GPIO.IN)
    
#     def readUltrasonic(self):
#         try:
#             GPIO.output(self.trigger_pin, GPIO.LOW)
#             time.sleep(0.000002)
#             GPIO.output(self.trigger_pin, GPIO.HIGH)
#             time.sleep(0.00001)
#             GPIO.output(self.trigger_pin, GPIO.LOW)
            
#             timeout = time.time() + 0.1
#             while GPIO.input(self.echo_pin) == GPIO.LOW:
#                 pulse_start = time.time()
#                 if pulse_start > timeout:
#                     return self.ULTRASONIC_ERROR_TIMEOUT
            
#             timeout = time.time() + 0.1
#             while GPIO.input(self.echo_pin) == GPIO.HIGH:
#                 pulse_end = time.time()
#                 if pulse_end > timeout:
#                     return self.ULTRASONIC_ERROR_TIMEOUT
            
#             pulse_duration = pulse_end - pulse_start
#             self.distance = (pulse_duration * 34300) / 2
#             return self.ULTRASONIC_OK
#         except Exception as e:
#             print(f"Error reading ultrasonic: {e}")
#             return self.ULTRASONIC_ERROR
    
#     def cleanup(self):
#         GPIO.cleanup([self.trigger_pin, self.echo_pin])

# def parseUltrasonicCheckCode(code):
#     if code == 0:
#         return "ULTRASONIC_OK"
#     elif code == -1:
#         return "ULTRASONIC_ERROR_TIMEOUT"
#     elif code == -2:
#         return "ULTRASONIC_ERROR"

# def run_ultrasonic_loop(ultrasonic, delay, callback, stop_event):
#     while True:
#         check = ultrasonic.readUltrasonic()
#         code = parseUltrasonicCheckCode(check)
#         distance = ultrasonic.distance
#         callback(distance, code)
#         if stop_event.is_set():
#             break
#         time.sleep(delay)
