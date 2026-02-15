import threading
import json
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT
import paho.mqtt.client as mqtt
from settings import load_settings

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


def led_callback(value, settings):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": "DL",
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": value,
    }

    with counter_lock:
        batch.append(("DL", json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def led_on(settings):
    print("[DL] LED turned ON")
    led_callback(1, settings)

def led_off(settings):
    print("[DL] LED turned OFF")
    led_callback(0, settings)

def on_command_received(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    if payload.get("action") == "ON":
        led_on(load_settings()["DL"])
    if payload.get("action") == "OFF":
        led_off(load_settings()["DL"])

cmd_client = mqtt.Client()
cmd_client.on_message = on_command_received
cmd_client.connect(HOSTNAME, PORT, 60)
cmd_client.subscribe("commands/DL")
cmd_client.loop_start()
