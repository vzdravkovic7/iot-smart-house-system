# import RPi.GPIO as GPIO
# import time

# class Membrane(object):
#     MEMBRANE_OK = 0
#     MEMBRANE_ERROR = -1
#     MEMBRANE_NO_KEY = -2
    
#     KEYPAD_MAP = {
#         ('R1', 'C1'): '1', ('R1', 'C2'): '2', ('R1', 'C3'): '3', ('R1', 'C4'): 'A',
#         ('R2', 'C1'): '4', ('R2', 'C2'): '5', ('R2', 'C3'): '6', ('R2', 'C4'): 'B',
#         ('R3', 'C1'): '7', ('R3', 'C2'): '8', ('R3', 'C3'): '9', ('R3', 'C4'): 'C',
#         ('R4', 'C1'): '*', ('R4', 'C2'): '0', ('R4', 'C3'): '#', ('R4', 'C4'): 'D',
#     }
    
#     def __init__(self, row_pins, col_pins):
#         self.row_pins = row_pins
#         self.col_pins = col_pins
#         self.key_pressed = None
#         GPIO.setmode(GPIO.BCM)
        
#         for pin in self.row_pins:
#             GPIO.setup(pin, GPIO.OUT)
#             GPIO.output(pin, GPIO.HIGH)
        
#         for pin in self.col_pins:
#             GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
#     def readMembrane(self):
#         try:
#             for row_idx, row_pin in enumerate(self.row_pins):
#                 GPIO.output(row_pin, GPIO.LOW)
                
#                 for col_idx, col_pin in enumerate(self.col_pins):
#                     if GPIO.input(col_pin) == GPIO.LOW:
#                         self.key_pressed = self.KEYPAD_MAP.get(
#                             (f'R{row_idx+1}', f'C{col_idx+1}'),
#                             None
#                         )
#                         GPIO.output(row_pin, GPIO.HIGH)
#                         return self.MEMBRANE_OK if self.key_pressed else self.MEMBRANE_NO_KEY
                
#                 GPIO.output(row_pin, GPIO.HIGH)
            
#             self.key_pressed = None
#             return self.MEMBRANE_NO_KEY
#         except Exception as e:
#             print(f"Error reading membrane: {e}")
#             return self.MEMBRANE_ERROR
    
#     def cleanup(self):
#         GPIO.cleanup(self.row_pins + self.col_pins)

# def parseMembraneCheckCode(code):
#     if code == 0:
#         return "MEMBRANE_OK"
#     elif code == -1:
#         return "MEMBRANE_ERROR"
#     elif code == -2:
#         return "MEMBRANE_NO_KEY"

# def run_membrane_loop(membrane, delay, callback, stop_event):
#     while True:
#         check = membrane.readMembrane()
#         code = parseMembraneCheckCode(check)
#         key = membrane.key_pressed
#         callback(key, code)
#         if stop_event.is_set():
#             break
#         time.sleep(delay)
