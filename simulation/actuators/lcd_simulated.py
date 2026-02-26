import json
import paho.mqtt.client as mqtt
from components.broker_settings import HOSTNAME, PORT
from settings import load_settings
import threading

def on_command_received(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    lcd = load_settings()["LCD"]
    if lcd["simulated"]:
        print("[LCD] DISPLAY MESSAGE: ", payload.get("display"))
    else:
        from actuators.LCD1602 import lcd_run
        print("Starting lcd1 loop")
        lcd1_thread = threading.Thread(target=lcd_run, args=(payload.get("display"), ))
        lcd1_thread.start()
        print("lcd1 loop started")

cmd_client = mqtt.Client()
cmd_client.on_message = on_command_received
cmd_client.connect(HOSTNAME, PORT, 60)
cmd_client.subscribe("commands/LCD")
cmd_client.loop_start()
