import threading
from simulators.membrane import run_membrane_simulator
# from sensors.membrane import Membrane, run_membrane_loop

def membrane_callback(key, code=None):
    if code:
        print(f"[DMS] Key pressed: {key} ({code})")
    else:
        print(f"[DMS] Key pressed: {key}")

def run_membrane(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_membrane_simulator, args=(4, membrane_callback, stop_event))
        t.start()
        threads.append(t)
    else:
        pass
        # row_pins = settings.get('row_pins', [20, 21, 22, 23])
        # col_pins = settings.get('col_pins', [24, 25, 26, 27])
        # membrane = Membrane(row_pins, col_pins)
        # t = threading.Thread(target=run_membrane_loop, args=(membrane, 0.2, membrane_callback, stop_event))
        # t.start()
        # threads.append(t)