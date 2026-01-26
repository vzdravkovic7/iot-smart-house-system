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


def buzzer_callback(value, settings):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": "DB",
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": value,
    }

    with counter_lock:
        batch.append(("DB", json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def buzzer_on(settings):
    print("[DB] Buzzer ACTIVATED")
    buzzer_callback(1, settings)


def buzzer_off(settings):
    print("[DB] Buzzer DEACTIVATED")
    buzzer_callback(0, settings)
