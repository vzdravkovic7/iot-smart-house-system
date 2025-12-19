import threading
from simulators.ultrasonic import run_ultrasonic_simulator
# from sensors.ultrasonic import Ultrasonic, run_ultrasonic_loop

def ultrasonic_callback(distance, code=None):
    if code:
        print(f"[DUS1] Distance: {distance:.1f} cm ({code})")
    else:
        print(f"[DUS1] Distance: {distance:.1f} cm")

def run_ultrasonic(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_ultrasonic_simulator, args=(2, ultrasonic_callback, stop_event))
        t.start()
        threads.append(t)
    else:
        pass
        # ultrasonic = Ultrasonic(settings['trigger_pin'], settings['echo_pin'])
        # t = threading.Thread(target=run_ultrasonic_loop, args=(ultrasonic, 1.0, ultrasonic_callback, stop_event))
        # t.start()
        # threads.append(t)