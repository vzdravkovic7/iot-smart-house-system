import threading
from simulators.pir import run_pir_simulator


def pir_callback(motion):
    print("[DPIR1] Motion:", "DETECTED" if motion else "NO MOTION")


def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_pir_simulator, args=(3, pir_callback, stop_event))
        t.start()
        threads.append(t)