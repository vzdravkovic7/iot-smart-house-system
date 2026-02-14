import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT

batch = []
publish_data_counter = 0
publish_data_limit = 1
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


def membrane_callback(pin, settings):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": "Membrane",
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": pin,
    }

    with counter_lock:
        batch.append(("Membrane", json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def membrane_input(settings):
    pin = input("Enter 4-digit PIN: ")
    if len(pin) == 4 and pin.isdigit():
        membrane_callback(pin, settings)
