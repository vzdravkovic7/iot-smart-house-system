import threading
from simulators.button import run_button_simulator
# from sensors.button import Button, run_button_loop

def button_callback(pressed, code=None):
    status = "PRESSED" if pressed else "RELEASED"
    if code:
        print(f"[DS1] Button: {status} ({code})")
    else:
        print(f"[DS1] Button: {status}")

def run_button(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_button_simulator, args=(2, button_callback, stop_event))
        t.start()
        threads.append(t)
    else:
        pass
        # button = Button(settings['pin'])
        # t = threading.Thread(target=run_button_loop, args=(button, 0.2, button_callback, stop_event))
        # t.start()
        # threads.append(t)