from simulators.gyro import run_gyro_simulator
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

def gyro_callback(x, y, z, settings, publish_event):
    global publish_data_counter, publish_data_limit

    base_payload = {
        "measurement": settings['measurement'],
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"]
    }

    x_pay = base_payload.copy()
    x_pay["name"] = f"{settings['name']}_x"
    x_pay["value"] = x
    
    y_pay = base_payload.copy()
    y_pay["name"] = f"{settings['name']}_y"
    y_pay["value"] = y

    z_pay = base_payload.copy()
    z_pay["name"] = f"{settings['name']}_z"
    z_pay["value"] = z

    with counter_lock:
        batch.append((settings['measurement'], json.dumps(x_pay), 0, True))
        batch.append((settings['measurement'], json.dumps(y_pay), 0, True))
        batch.append((settings['measurement'], json.dumps(z_pay), 0, True))
        
        publish_data_counter += 3

    if publish_data_counter >= publish_data_limit:
        publish_event.set()


def run_gyro(settings, threads, stop_event):
    if settings["simulated"]:
        t = threading.Thread(
            target=run_gyro_simulator,
            args=(1, gyro_callback, stop_event, publish_event, settings)
        )
        t.start()
        threads.append(t)
    else:
        pass