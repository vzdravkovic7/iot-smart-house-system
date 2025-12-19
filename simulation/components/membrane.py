import threading
from simulators.membrane import run_membrane_simulator


def membrane_callback(key):
    print(f"[DMS] Key pressed: {key}")


def run_membrane(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_membrane_simulator, args=(4, membrane_callback, stop_event))
        t.start()
        threads.append(t)