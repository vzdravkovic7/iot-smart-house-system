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

def dht_callback(humidity, temperature, publish_event, settings):
    global publish_data_counter, publish_data_limit

    base_payload = {
        "measurement": settings['measurement'],
        "simulated": settings['simulated'],
        "runs_on": settings["runs_on"]
    }

    h_pay = base_payload.copy()
    h_pay["name"] = f"{settings['name']}_humidity"
    h_pay["value"] = float(humidity)
    
    t_pay = base_payload.copy()
    t_pay["name"] = f"{settings['name']}_temperature"
    t_pay["value"] = float(temperature)

    with counter_lock:
        batch.append((settings['measurement'], json.dumps(h_pay), 0, True))
        batch.append((settings['measurement'], json.dumps(t_pay), 0, True))
        
        publish_data_counter += 2

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(3, dht_callback, stop_event, publish_event, settings))
            dht1_thread.start()
            threads.append(dht1_thread)
        else:
            from sensors.dht import run_dht_loop, DHT
            print("Starting dht1 loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dht_callback, stop_event, settings))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 loop started")
