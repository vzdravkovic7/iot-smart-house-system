from simulators.dht import run_dht_simulator
import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT

batch = []
publish_data_counter = 0
publish_data_limit = 5
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


def dht_callback(temp, hum, settings, publish_event):
    global publish_data_counter, publish_data_limit

    base_payload = {
        "measurement": settings['measurement'],
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"]
    }

    h_pay = base_payload.copy()
    h_pay["name"] = f"{settings['name']}_humidity"
    h_pay["value"] = hum
    
    t_pay = base_payload.copy()
    t_pay["name"] = f"{settings['name']}_temperature"
    t_pay["value"] = temp

    with counter_lock:
        batch.append((settings['measurement'], json.dumps(h_pay), 0, True))
        batch.append((settings['measurement'], json.dumps(t_pay), 0, True))
        
        publish_data_counter += 2

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_dht(settings, threads, stop_event):
    if settings["simulated"]:
        t = threading.Thread(
            target=run_dht_simulator,
            args=(5, dht_callback, stop_event, publish_event, settings)
        )
        t.start()
        threads.append(t)
    else:
        pass
        # real dht