import threading
import time
from settings import load_settings
from components.button import run_button
from components.pir import run_pir
from components.ultrasonic import run_ultrasonic
from components.membrane import run_membrane
from actuators.led import led_on, led_off
from actuators.buzzer import buzzer_on, buzzer_off




def console_menu():
    print("\n=== ACTUATOR CONTROL ===")
    print("1 - LED ON")
    print("2 - LED OFF")
    print("3 - BUZZER ON")
    print("4 - BUZZER OFF")
    print("q - Quit")




if __name__ == "__main__":
    print("Starting KT1 Smart Door Simulation")
    settings = load_settings()
    threads = []
    stop_event = threading.Event()


    try:
        run_button(settings['DS1'], threads, stop_event)
        run_pir(settings['DPIR1'], threads, stop_event)
        run_ultrasonic(settings['DUS1'], threads, stop_event)
        run_membrane(settings['DMS'], threads, stop_event)


        while True:
            console_menu()
            cmd = input("> ")


            if cmd == "1":
                led_on()
            elif cmd == "2":
                led_off()
            elif cmd == "3":
                buzzer_on()
            elif cmd == "4":
                buzzer_off()
            elif cmd.lower() == "q":
                break


    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping application")
        stop_event.set()
        for t in threads:
            t.join()