import threading
from simulators.pir import run_pir_simulator
# from sensors.pir import PIR, run_pir_loop

def pir_callback(motion, code=None):
    status = "DETECTED" if motion else "NO MOTION"
    if code:
        print(f"[DPIR1] Motion: {status} ({code})")
    else:
        print(f"[DPIR1] Motion: {status}")

def run_pir(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_pir_simulator, args=(3, pir_callback, stop_event))
        t.start()
        threads.append(t)
    else:
        pass
        # pir = PIR(settings['pin'])
        # t = threading.Thread(target=run_pir_loop, args=(pir, 0.5, pir_callback, stop_event))
        # t.start()
        # threads.append(t)