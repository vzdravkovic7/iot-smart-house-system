import threading
from settings import load_settings
from components.button import run_button
from components.pir import run_pir
from components.ultrasonic import run_ultrasonic
from components.membrane import run_membrane
from components.dht import run_dht
from components.ir import run_ir
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
    print("Starting Smart House")
    settings = load_settings()
    threads = []
    stop_event = threading.Event()

    try:
        # run_button(settings['DS1'], threads, stop_event)
        # run_pir(settings['DPIR1'], threads, stop_event)
        # run_ultrasonic(settings['DUS1'], threads, stop_event)
        # run_membrane(settings['DMS'], threads, stop_event)

        # run_dht(settings['DHT1'], threads, stop_event)
        # run_dht(settings['DHT2'], threads, stop_event)
        # run_ir(settings['IR'], threads, stop_event)
        # run_ir(settings['LCD'], threads, stop_event)
        # run_pir(settings['DPIR3'], threads, stop_event)


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
            elif cmd.lower() == "q":
                break

    except KeyboardInterrupt:
        pass
    finally:
        print("Stopping application")
        stop_event.set()
        for t in threads:
            t.join()