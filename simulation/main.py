import threading
from settings import load_settings
from components.generic_button import run_generic_button
from components.pir import run_pir
from components.ultrasonic import run_ultrasonic
from actuators.membrane import membrane_input
from components.dht import run_dht
from components.ir import run_ir
from components.gyro import run_gyro
from actuators.led import led_on, led_off
from actuators.buzzer import buzzer_on, buzzer_off
from actuators.timer4sd import timer_set, timer_clear
from components.web_camera import run_web_camera
from actuators.lcd_simulated import *
from actuators.brgb import *

def console_menu():
    print("\n=== ACTUATOR CONTROL ===")
    print("1 - LED ON")
    print("2 - LED OFF")
    print("3 - BUZZER ON")
    print("4 - BUZZER OFF")
    print("5 - SET TIMER VALUE")
    print("6 - CLEAR TIMER")
    print("7 - Enter pin")
    print("q - Quit")

if __name__ == "__main__":
    print("Starting Smart House")
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        run_dht(settings['DHT1'], threads, stop_event)
        run_dht(settings['DHT2'], threads, stop_event)
        run_ir(settings['IR'], threads, stop_event)
        run_ir(settings['LCD'], threads, stop_event)
        run_pir(settings['DPIR3'], settings['DL'], threads, stop_event)

        run_generic_button(settings['DS1'], threads, stop_event)
        run_generic_button(settings['DS2'], threads, stop_event)
        run_generic_button(settings['BTN'], threads, stop_event)
        run_pir(settings['DPIR1'], settings['DL'], threads, stop_event)
        run_pir(settings["DPIR2"], settings['DL'], threads, stop_event)
        run_ultrasonic(settings['DUS1'], threads, stop_event)
        run_ultrasonic(settings["DUS2"], threads, stop_event)
        run_dht(settings["DHT3"], threads, stop_event)
        run_gyro(settings["GSG"], threads, stop_event)
        run_web_camera(settings["WEBC"], threads, stop_event)

        while True:
            console_menu()
            cmd = input("> ")

            if cmd == "1":
                led_on(settings['DL'])
            elif cmd == "2":
                led_off(settings['DL'])
            elif cmd == "3":
                buzzer_on(settings['DB'])
            elif cmd == "4":
                buzzer_off(settings['DB'])
            elif cmd == "5":
                value = int(input("Enter timer value: "))
                timer_set(settings['4SD'], value)
            elif cmd == "6":
                timer_clear(settings['4SD'])
            elif cmd == "7":
                membrane_input(settings['DMS'])
            elif cmd.lower() == "q":
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping application")
        stop_event.set()
        for t in threads:
            t.join()