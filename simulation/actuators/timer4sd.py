import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT

batch = []
publish_data_counter = 0
publish_data_limit = 2
counter_lock = threading.Lock()

def publisher_task(event, batch):
    global publish_data_counter, publish_data_limit
    while True:
        event.wait()
        with counter_lock:
            local_batch = batch.copy()
            publish_data_counter = 0
            batch.clear()

        publish.multiple(local_batch, hostname=HOSTNAME, port=PORT)
        event.clear()


publish_event = threading.Event()
publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch,))
publisher_thread.daemon = True
publisher_thread.start()


def timer_callback(value, settings):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": "4SD",
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": value
    }

    with counter_lock:
        batch.append(("4SD", json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def timer_set(settings, value):
    print(f"[4SD] Timer set to {value}")
    timer_callback(value, settings)


def timer_clear(settings):
    print("[4SD] Timer cleared")
    timer_callback(0, settings)
