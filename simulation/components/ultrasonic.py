import threading
from simulators.ultrasonic import run_ultrasonic_simulator
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT

batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

def publisher_task(event, batch):
    global publish_data_counter
    while True:
        event.wait()
        with counter_lock:
            local_batch = batch.copy()
            batch.clear()
            publish_data_counter = 0
        publish.multiple(local_batch, hostname=HOSTNAME, port=PORT)
        event.clear()

publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch))
publisher_thread.daemon = True
publisher_thread.start()

def ultrasonic_callback(distance, settings, publish_event):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": settings["measurement"],
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": distance
    }

    with counter_lock:
        batch.append((settings["measurement"], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_ultrasonic(settings, threads, stop_event):
    if settings["simulated"]:
        t = threading.Thread(
            target=run_ultrasonic_simulator,
            args=(3, ultrasonic_callback, stop_event, publish_event, settings)
        )
        t.start()
        threads.append(t)
    else:
        pass
        # ultrasonic = Ultrasonic(settings['trigger_pin'], settings['echo_pin'])
        # t = threading.Thread(target=run_ultrasonic_loop, args=(ultrasonic, 1.0, ultrasonic_callback, stop_event))
        # t.start()
        # threads.append(t)