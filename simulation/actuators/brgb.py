import json
import threading
import paho.mqtt.client as mqtt
from components.broker_settings import HOSTNAME, PORT
from settings import load_settings

def on_command_received(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    settings = load_settings()["BRGB"]

    mode = payload.get("action")

    if settings["simulated"]:
        if mode == 0:
            print("[BRGB] DIODE OFF")
        elif mode == 1:
            print("[BRGB] DIODE WHITE")
        elif mode == 2:
            print("[BRGB] DIODE RED")
        elif mode == 3:
            print("[BRGB] DIODE GREEN")
        elif mode == 4:
            print("[BRGB] DIODE BLUE")

    else:
        from actuators.rgb_led import rgb_run

        print("Starting real RGB action")

        t = threading.Thread(
            target=rgb_run,
            args=(mode, settings)
        )
        t.start()


cmd_client = mqtt.Client()
cmd_client.on_message = on_command_received
cmd_client.connect(HOSTNAME, PORT, 60)
cmd_client.subscribe("commands/BRGB")
cmd_client.loop_start()