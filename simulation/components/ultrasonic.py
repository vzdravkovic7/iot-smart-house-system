import threading
from simulators.ultrasonic import run_ultrasonic_simulator


def ultrasonic_callback(distance):
    print(f"[DUS1] Distance: {distance:.1f} cm")


def run_ultrasonic(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_ultrasonic_simulator, args=(2, ultrasonic_callback, stop_event))
        t.start()
        threads.append(t)