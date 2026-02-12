import RPi.GPIO as GPIO
import time
from datetime import datetime

class IR(object):
    IRLIB_OK = 0
    IRLIB_ERROR_TIMEOUT = -2
    IRLIB_IGNORE = -4
    
    def __init__(self, pin):
        self.pin = pin
        self.is_on = False
        
        self.POWER_BUTTON_HEX = "0x300ff02fd" 
        
        GPIO.setup(self.pin, GPIO.IN)

    def getBinary(self):
        num1s = 0
        binary = 1
        command = []
        previousValue = 0
        value = GPIO.input(self.pin)

        wait_start = time.time()
        while value:
            if time.time() - wait_start > 1.0:
                return None
            time.sleep(0.0001)
            value = GPIO.input(self.pin)

        startTime = datetime.now()
        while True:
            if previousValue != value:
                now = datetime.now()
                pulseTime = now - startTime
                startTime = now
                command.append((previousValue, pulseTime.microseconds))
            if value: num1s += 1
            else: num1s = 0
            if num1s > 10000: break
            previousValue = value
            value = GPIO.input(self.pin)

        for (typ, tme) in command:
            if typ == 1:
                if tme > 1000: binary = binary * 10 + 1
                else: binary *= 10
        
        if len(str(binary)) > 34:
            binary = int(str(binary)[:34])
        return binary

    def toggle(self):
        binaryValue = self.getBinary()
        if binaryValue is None:
            return self.IRLIB_ERROR_TIMEOUT

        try:
            tmpB2 = int(str(binaryValue), 2)
            inData = hex(tmpB2)
        except ValueError:
            return self.IRLIB_ERROR_TIMEOUT

        if inData == self.POWER_BUTTON_HEX:
            self.is_on = not self.is_on
            return self.IRLIB_OK
        
        return self.IRLIB_IGNORE

def run_ir_loop(ir, delay, callback, stop_event):
    while not stop_event.is_set():
        check = ir.toggle()
        
        status_code = "OK" if check == 0 else "IDLE"
        
        callback(ir.is_on, status_code)
        
        time.sleep(delay)