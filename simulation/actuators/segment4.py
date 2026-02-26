#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

segments = (11, 4, 23, 8, 7, 10, 18, 25)

for segment in segments:
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

digits = (22, 27, 17, 24)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

num = {
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '0': (1, 1, 1, 1, 1, 1, 0),
    '1': (0, 1, 1, 0, 0, 0, 0),
    '2': (1, 1, 0, 1, 1, 0, 1),
    '3': (1, 1, 1, 1, 0, 0, 1),
    '4': (0, 1, 1, 0, 0, 1, 1),
    '5': (1, 0, 1, 1, 0, 1, 1),
    '6': (1, 0, 1, 1, 1, 1, 1),
    '7': (1, 1, 1, 0, 0, 0, 0),
    '8': (1, 1, 1, 1, 1, 1, 1),
    '9': (1, 1, 1, 1, 0, 1, 1)
}

display_lock = threading.Lock()
current_display = "0000"
display_active = True
blink_active = False

def _display_digit(digit_index, digit_char, show_colon=False):
    for loop in range(7):
        GPIO.output(segments[loop], num[digit_char][loop])
    
    if show_colon and digit_index == 1:
        GPIO.output(25, 1)
    else:
        GPIO.output(25, 0)
    
    GPIO.output(digits[digit_index], 0)
    time.sleep(0.001)
    GPIO.output(digits[digit_index], 1)

def _refresh_display(duration=0.1):
    global current_display
    end_time = time.time() + duration
    
    while time.time() < end_time and display_active:
        with display_lock:
            s = current_display
        
        for digit in range(4):
            if digit < len(s):
                _display_digit(digit, s[digit], show_colon=True)

def display_time(minutes, seconds):
    global current_display, blink_active
    
    blink_active = False
    
    time_str = f"{minutes:02d}{seconds:02d}"
    
    with display_lock:
        current_display = time_str
    
    _refresh_display(0.05)

def blink_display():
    global current_display, blink_active, display_active
    
    blink_active = True
    
    print("[4SD REAL] Starting blink...")
    
    while blink_active and display_active:
        with display_lock:
            current_display = "0000"
        _refresh_display(0.5)
        
        if not blink_active:
            break
        
        with display_lock:
            current_display = "    "
        _refresh_display(0.5)

def clear_display():
    global current_display, blink_active
    
    blink_active = False
    
    with display_lock:
        current_display = "    "
    
    _refresh_display(0.1)
    
    for segment in segments:
        GPIO.output(segment, 0)
    for digit in digits:
        GPIO.output(digit, 1)

def cleanup():
    global display_active
    display_active = False
    time.sleep(0.2)
    GPIO.cleanup()

if __name__ == '__main__':
    print('4-Segment Display Test')
    try:
        for i in range(10, -1, -1):
            minutes = i // 60
            seconds = i % 60
            display_time(minutes, seconds)
            time.sleep(1)
        
        print("Blinking for 5 seconds...")
        blink_thread = threading.Thread(target=blink_display)
        blink_thread.start()
        time.sleep(5)
        blink_active = False
        blink_thread.join()
        
        clear_display()
        
    except KeyboardInterrupt:
        pass
    finally:
        cleanup()