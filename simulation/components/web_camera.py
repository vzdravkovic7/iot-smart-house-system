from simulators.web_camera import run_web_camera_simulator
import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT

batch = []
publish_data_counter = 0
publish_data_limit = 5
counter_lock = threading.Lock()
publish_event = threading.Event()

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

publisher_thread = threading.Thread(target=publisher_task, args=(publish_event, batch))
publisher_thread.daemon = True
publisher_thread.start()

def web_camera_callback(motion, settings, publish_event):
    global publish_data_counter
    payload = {
        "measurement": settings["measurement"],
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": motion
    }

    with counter_lock:
        batch.append((settings["measurement"], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_web_camera(settings, threads, stop_event):
    if settings["simulated"]:
        t = threading.Thread(
            target=run_web_camera_simulator,
            args=(3, web_camera_callback, stop_event, publish_event, settings)
        )
        t.start()
        threads.append(t)
    else:
        pass
