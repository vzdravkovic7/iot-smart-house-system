from simulators.ir import run_ir_simulator
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

def ir_callback(code, publish_event, settings):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": settings['measurement'],
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": code
    }

    with counter_lock:
        batch.append((settings['measurement'], json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_ir(settings, threads, stop_event):
        if settings['simulated']:
            ir1_thread = threading.Thread(target = run_ir_simulator, args=(5, ir_callback, stop_event, publish_event, settings))
            ir1_thread.start()
            threads.append(ir1_thread)
        else:
            from sensors.ir import run_ir_loop, IR
            print("Starting ir loop")
            ir = IR(settings['pin'])
            ir1_thread = threading.Thread(target=run_ir_loop, args=(ir, 2, ir_callback, stop_event))
            ir1_thread.start()
            threads.append(ir1_thread)
            print("ir1 loop started")
