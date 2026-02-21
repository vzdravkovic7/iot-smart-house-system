import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT
from settings import load_settings

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


def membrane_callback(pin, settings):
    global publish_data_counter

    payload = {
        "measurement": settings["measurement"],
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": pin,
    }

    with counter_lock:
        batch.append((settings["measurement"], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def membrane_input(settings):
    pin = input("Enter 4-digit PIN: ")
    if len(pin) == 4 and pin.isdigit():
        membrane_callback(pin, settings)


def run_membrane(settings, stop_event, threads):
    if settings["simulated"]:
        t = threading.Thread(target=membrane_input, args=(settings,))
        t.start()
        threads.append(t)
    else:
        from actuators.tastatura import keypad_run

        t = threading.Thread(
            target=keypad_run,
            args=(settings, membrane_callback, stop_event)
        )
        t.start()
        threads.append(t)