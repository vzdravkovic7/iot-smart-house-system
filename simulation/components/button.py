import threading
from simulators.button import run_button_simulator


def button_callback(pressed):
    print("[DS1] Button:", "PRESSED" if pressed else "RELEASED")


def run_button(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_button_simulator, args=(2, button_callback, stop_event))
        t.start()
        threads.append(t)