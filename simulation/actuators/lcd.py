import json
import paho.mqtt.client as mqtt
from components.broker_settings import HOSTNAME, PORT

def on_command_received(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    print("[LCD] DISPLAY MESSAGE: ", payload.get("display"))

cmd_client = mqtt.Client()
cmd_client.on_message = on_command_received
cmd_client.connect(HOSTNAME, PORT, 60)
cmd_client.subscribe("commands/LCD")
cmd_client.loop_start()
