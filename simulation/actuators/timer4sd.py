import threading
import json
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from components.broker_settings import HOSTNAME, PORT
from settings import load_settings

batch = []
publish_data_counter = 0
publish_data_limit = 1
counter_lock = threading.Lock()

current_timer_value = 0
timer_running = False
timer_thread = None
is_blinking = False

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

def timer_callback(value, settings):
    global publish_data_counter, publish_data_limit

    payload = {
        "measurement": "4SD",
        "simulated": settings["simulated"],
        "runs_on": settings["runs_on"],
        "name": settings["name"],
        "value": value
    }

    with counter_lock:
        batch.append(("4SD", json.dumps(payload), 0, True))
        publish_data_counter += 1

    if publish_data_counter >= publish_data_limit:
        publish_event.set()

def real_timer_countdown(initial_value, settings):
    global current_timer_value, timer_running, is_blinking
    
    from actuators.segment4 import display_time, blink_display, clear_display
    
    current_timer_value = initial_value
    timer_running = True
    is_blinking = False
    
    print(f"[4SD REAL] Starting countdown from {initial_value} seconds")
    
    while current_timer_value > 0 and timer_running:
        minutes = current_timer_value // 60
        seconds = current_timer_value % 60
        display_time(minutes, seconds)
        timer_callback(current_timer_value, settings)
        time.sleep(1)
        current_timer_value -= 1
    
    if timer_running:
        print("[4SD REAL] Timer finished - blinking")
        is_blinking = True
        timer_callback(0, settings)
        blink_display()

def timer_set(settings, value):
    global timer_thread, timer_running, is_blinking
    
    timer_running = False
    is_blinking = False
    if timer_thread and timer_thread.is_alive():
        timer_thread.join(timeout=2)
    
    timer_callback(value, settings)
    
    if settings["simulated"]:
        print(f"[4SD SIMULATED] Timer set to {value} seconds")
    else:
        timer_thread = threading.Thread(target=real_timer_countdown, args=(value, settings))
        timer_thread.daemon = True
        timer_thread.start()

def timer_blink():
    global is_blinking
    print(f"[4SD] Manual Blink command")
    settings = load_settings()["4SD"]
    
    if not settings["simulated"]:
        from actuators.segment4 import blink_display
        is_blinking = True
        blink_thread = threading.Thread(target=blink_display)
        blink_thread.daemon = True
        blink_thread.start()

def timer_clear(settings):
    global timer_running, is_blinking, current_timer_value
    
    print("[4SD] Timer cleared/stopped")
    timer_running = False
    is_blinking = False
    current_timer_value = 0
    timer_callback(0, settings)
    
    if not settings["simulated"]:
        from actuators.segment4 import clear_display
        clear_display()

def on_command_received(client, userdata, msg):
    payload = json.loads(msg.payload.decode('utf-8'))
    settings = load_settings()["4SD"]
    
    if payload.get("blink") == -1:
        timer_blink()
    elif payload.get("stopwatch") is not None:
        stopwatch_value = int(payload.get("stopwatch"))
        if stopwatch_value == 0:
            timer_clear(settings)
        else:
            timer_set(settings, stopwatch_value)
    elif payload.get("clear"):
        timer_clear(settings)

cmd_client = mqtt.Client()
cmd_client.on_message = on_command_received
cmd_client.connect(HOSTNAME, PORT, 60)
cmd_client.subscribe("commands/4SD")
cmd_client.loop_start()