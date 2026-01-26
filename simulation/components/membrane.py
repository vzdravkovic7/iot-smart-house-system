import threading
from simulators.membrane import run_membrane_simulator
# from sensors.membrane import Membrane, run_membrane_loop
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT

batch = []
publish_data_counter = 0
publish_data_limit = 5
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

def membrane_callback(key, settings, publish_event):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": "Membrane",
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": key
    }

    with counter_lock:
        batch.append(('Membrane', json.dumps(payload), 0, True))
        publish_data_counter += 1
    
    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_membrane(settings, threads, stop_event):
    if settings['simulated']:
        t = threading.Thread(target=run_membrane_simulator,
                             args=(4, membrane_callback, stop_event, publish_event, settings))
        t.start()
        threads.append(t)
    else:
        pass
        # row_pins = settings.get('row_pins', [20, 21, 22, 23])
        # col_pins = settings.get('col_pins', [24, 25, 26, 27])
        # membrane = Membrane(row_pins, col_pins)
        # t = threading.Thread(target=run_membrane_loop, args=(membrane, 0.2, membrane_callback, stop_event))
        # t.start()
        # threads.append(t)