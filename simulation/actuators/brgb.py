import json
import paho.mqtt.client as mqtt
from components.broker_settings import HOSTNAME, PORT

def on_command_received(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    mode = payload.get("action")
    if mode == 0:
        print("[BRGB] DIODE OFF")
    elif mode == 1:
        print("[BRGB] DIODE ON")
    elif mode == 2:
        print("[BRGB] DIODE LIGHT: RED")
    elif mode == 3:
        print("[BRGB] DIODE LIGHT: GREEN")
    elif mode == 4:
        print("[BRGB] DIODE LIGHT: BLUE")

cmd_client = mqtt.Client()
cmd_client.on_message = on_command_received
cmd_client.connect(HOSTNAME, PORT, 60)
cmd_client.subscribe("commands/BRGB")
cmd_client.loop_start()
