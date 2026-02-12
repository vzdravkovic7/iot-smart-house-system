import smbus
import time

class LCD(object):
    LCDLIB_OK = 0
    LCDLIB_ERROR_I2C = -1
    
    def __init__(self, address):
        self.bus = smbus.SMBus(1)
        self.address = address
        self.currentValue = 0
        self.backlight_state = 0
        
        try:
            self.writeByte(0)
        except:
            print(f"Greška: Ne mogu da pristupim LCD-u na adresi {hex(address)}")

    def writeByte(self, value):
        self.currentValue = value
        self.bus.write_byte(self.address, value)

    def digitalWrite(self, pin, newvalue):
        value = self.currentValue
        if newvalue == 1:
            value |= (1 << pin)
        elif newvalue == 0:
            value &= ~(1 << pin)
        self.writeByte(value)

    def readByte(self):
        return self.currentValue

    def set_backlight(self, state):
        self.backlight_state = 1 if state else 0
        self.digitalWrite(3, self.backlight_state)

    def check_status(self):
        try:
            self.bus.write_quick(self.address)
            return self.LCDLIB_OK
        except:
            return self.LCDLIB_ERROR_I2C

def parseLCDCheckCode(code):
    if code == 0:
        return "LCD_OK"
    else:
        return "LCD_ERROR_I2C"

def run_lcd_loop(lcd, delay, callback, stop_event):
    while True:
        check = lcd.check_status()
        code = parseLCDCheckCode(check)
        
        callback(lcd.backlight_state, lcd.currentValue, code)
        
        if stop_event.is_set():
            break
            
        time.sleep(delay)