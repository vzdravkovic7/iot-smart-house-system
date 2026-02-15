from state_manager import update_state, get_all_state, get_state
from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from flask_cors import CORS
import threading
import math
import time

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# InfluxDB Configuration
token = "9j45ZmqnOGoSx4XKPadoMPyot0zsX0DwZg3FpvuaDpKDFIuBomlqMCYTyT_CdRiTBjtijnb9qJXw8-9XIrH9zg=="
org = "FTN"
url = "http://localhost:8086"
bucket = "example_db"
influxdb_client = InfluxDBClient(url=url, token=token, org=org)

# MQTT Configuration
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883, 60)
mqtt_client.loop_start()

def on_connect(client, userdata, flags, rc):
    client.subscribe("Button"),
    client.subscribe("DS2"),
    client.subscribe("BTN"),
    client.subscribe("PIR"),
    client.subscribe("PIR2"),
    client.subscribe("Ultrasonic"),
    client.subscribe("Ultrasonic2"),
    client.subscribe("Membrane"),
    client.subscribe("DHT3"),
    client.subscribe("GSG"),
    client.subscribe("WEBC"),
    client.subscribe("DL"),
    client.subscribe("DB"),
    client.subscribe("DHT1"),
    client.subscribe("DHT2"),
    client.subscribe("IR"),
    client.subscribe("LCD"),
    client.subscribe("DPIR3"),
    client.subscribe("4SD")

mqtt_client.on_connect = on_connect

def on_message(client, userdata, msg):
    parsed = json.loads(msg.payload.decode('utf-8'))

    if isinstance(parsed, list):
        for data in parsed:
            process_data(data)
    else:
        process_data(parsed)

last_dus1_value = None
last_dus2_value = None
buzzer_active = False
LED_active = False
system_armed = False
system_pin = 1312
people_count = 0
ALARM = False
door_timers = {}
last_gsg_magnitude = None
gsg_threshold = 3.0
current_dht_index = 0
stopwatch = 0
blinking = False
N = 0

dht_names = [
    ("Bedroom DHT_temperature", "Bedroom DHT_humidity"),
    ("Master Bedroom DHT_temperature", "Master Bedroom DHT_humidity"),
    ("Kitchen DHT Sensor_temperature", "Kitchen DHT Sensor_humidity")
]

def process_data(data):
    global last_dus1_value, last_dus2_value, people_count, LED_active, stopwatch, blinking, N, ALARM

    update_state(
        measurement=data["measurement"],
        name=data["name"],
        value=data["value"],
        runs_on=data["runs_on"],
        simulated=data["simulated"]
    )

    if data["name"] in ["Kitchen Button"] and data["value"] == 1:
        if blinking:
            blinking = False
            mqtt_client.publish("commands/4SD", json.dumps({"stopwatch": 0}))
        else:
            stopwatch += N

    if data["name"] in ["Gyroscope Sensor_x", "Gyroscope Sensor_y", "Gyroscope Sensor_z"]:
        handle_gsg_motion()

    if data["name"] in ["Door Membrane Switch 1"]:
        timer = threading.Timer(2.0, arm_system, args=(data["value"],))
        timer.start()

    if data["name"] in ["Door Motion Sensor 1", "Door Motion Sensor 2", "Living Room Motion Sensor"] and data["value"] == 1 and people_count == 0:
        activate_alarm()

    if data["name"] in ["Door Motion Sensor 1", "Door Motion Sensor 2"] and data["value"] == 1:
        dus_state1 = get_state("Door Ultrasonic Sensor 1")
        dus_state2 = get_state("Door Ultrasonic Sensor 2")

        if not LED_active:
            LED_active = not LED_active
            mqtt_client.publish("commands/DL", json.dumps({"action": "ON"}))
    
            timer = threading.Timer(10.0, led_off)
            timer.start()

        if dus_state1 and last_dus1_value is not None:
            current_dist = dus_state1['value']
            
            if last_dus1_value > current_dist + 10:
                people_count += 1
                save_people_count(people_count)
                
            elif last_dus1_value < current_dist - 10:
                people_count = max(0, people_count - 1)
                save_people_count(people_count)

        if dus_state1:
            last_dus1_value = dus_state1['value']

        # dus2
        if dus_state2 and last_dus2_value is not None:
            current_dist = dus_state2['value']
            
            if last_dus2_value > current_dist + 10:
                people_count += 1
                save_people_count(people_count)
                
            elif last_dus2_value < current_dist - 10:
                people_count = max(0, people_count - 1)
                save_people_count(people_count)

        if dus_state2:
            last_dus2_value = dus_state2['value']

    if data["name"] in ["Door Sensor 1", "Door Sensor 2"]:
        sensor_name = data["name"]
        door_open = data["value"]

        if door_open == 1:
            if system_armed:
                activate_alarm()
            elif sensor_name not in door_timers or not door_timers[sensor_name].is_alive():
                t = threading.Timer(5.0, activate_alarm)
                door_timers[sensor_name] = t
                t.start()
        else:
            if sensor_name in door_timers:
                door_timers[sensor_name].cancel()
                del door_timers[sensor_name]
            
            if ALARM and not system_armed:
                deactivate_alarm()

    save_to_db(data)

def save_people_count(count):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = Point("PEOPLE_COUNT").field("value", count)
    write_api.write(bucket=bucket, org=org, record=point)

def led_off():
    global LED_active
    
    LED_active = not LED_active
    mqtt_client.publish("commands/DL", json.dumps({"action": "OFF"}))

def activate_buzzer(isOn):
    global buzzer_active

    if not buzzer_active and isOn:
        buzzer_active = not buzzer_active
        mqtt_client.publish("commands/DB", json.dumps({"action": buzzer_active}))
    elif buzzer_active and not isOn:
        buzzer_active = not buzzer_active
        mqtt_client.publish("commands/DB", json.dumps({"action": buzzer_active}))

def arm_system(pin):
    global system_armed

    if int(pin) == system_pin:
        system_armed = not system_armed
        update_state(
            measurement="system_armed",
            name="system_armed",
            value=int(system_armed),
            runs_on="Server",
            simulated=True
        )
        save_to_db({"measurement": "system_armed", "name": "Security System", "value": int(system_armed), "simulated": True, "runs_on": "Server"})
        deactivate_alarm()

def deactivate_alarm():
    global ALARM
    ALARM = False
    activate_buzzer(False)
    update_state(
        measurement="ALARM",
        name="ALARM",
        value=0,
        runs_on="Server",
        simulated=True
    )
    save_to_db({"measurement": "ALARM", "name": "Security System", "value": 0, "simulated": True, "runs_on": "Server"})

def activate_alarm():
    global ALARM
    ALARM = True

    activate_buzzer(True)

    payload = {
        "measurement": "ALARM",
        "name": "ALARM",
        "value": 1,
        "simulated": True,
        "runs_on": "Server"
    }
    update_state(
        measurement="ALARM",
        name="ALARM",
        value=1,
        runs_on="Server",
        simulated=True
    )
    save_to_db(payload)

mqtt_client.on_message = on_message

def handle_gsg_motion():
    global last_gsg_magnitude, gsg_threshold
    
    gx = get_state("Gyroscope Sensor_x")
    gy = get_state("Gyroscope Sensor_y")
    gz = get_state("Gyroscope Sensor_z")

    if not gx or not gy or not gz:
        return

    x = gx["value"]
    y = gy["value"]
    z = gz["value"]

    magnitude = math.sqrt(x*x + y*y + z*z)

    if last_gsg_magnitude is None:
        last_gsg_magnitude = magnitude
        return

    diff = abs(magnitude - last_gsg_magnitude)

    last_gsg_magnitude = magnitude

    if diff > gsg_threshold:
        activate_alarm()

def show_next_dht_on_stopwatch():
    global stopwatch

    if stopwatch > 0:
        mqtt_client.publish("commands/4SD", json.dumps({"stopwatch": stopwatch}))

def show_next_dht_on_lcd():
    global current_dht_index

    temp_key, hum_key = dht_names[current_dht_index]

    tem = get_state(temp_key)
    hum = get_state(hum_key)

    if tem and hum:
        temperature = tem["value"]
        humidity = hum["value"]
        text = f"DHT{current_dht_index+1}: Temp={temperature}°C | Hum={humidity}%"
    else:
        text = f"DHT{current_dht_index+1}: No data"

    mqtt_client.publish("commands/LCD", json.dumps({"display": text}))

    current_dht_index = (current_dht_index + 1) % 3

def save_to_db(data):
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    point = (
        Point(data["measurement"])
        .tag("simulated", data["simulated"])
        .tag("runs_on", data["runs_on"])
        .tag("name", data["name"])
        .field("measurement", data["value"])
    )
    write_api.write(bucket=bucket, org=org, record=point)


# Route to store dummy data
@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        store_data(data)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


def handle_influx_query(query):
    try:
        query_api = influxdb_client.query_api()
        tables = query_api.query(query, org=org)

        container = []
        for table in tables:
            for record in table.records:
                container.append(record.values)

        return jsonify({"status": "success", "data": container})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Button")"""
    return handle_influx_query(query)


@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    query = f"""from(bucket: "{bucket}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Button")
    |> mean()"""
    return handle_influx_query(query)

@app.route("/api/state", methods=["GET"])
def api_all_state():
    return jsonify(get_all_state())

@app.route("/api/alarm", methods=["GET"])
def switch_alarm():
    global ALARM
    deactivate_alarm() if ALARM else activate_alarm()
    return jsonify(True)

@app.route("/api/system", methods=["GET"])
def switch_system():
    arm_system(1312)
    return jsonify(True)

@app.route("/api/stopwatch", methods=["POST"])
def updateStopwatch():
    global N
    N = int(request.json['stopwatch'])
    
    return jsonify(True)

@app.route("/api/state/<name>", methods=["GET"])
def api_device_state(name):
    result = get_state(name)
    if result is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(result)

def lcd_rotation_loop():
    while True:
        show_next_dht_on_lcd()
        time.sleep(4)

def stopwatch_background_loop():
    global stopwatch, blinking
    while True:
        if stopwatch > 0:
            blinking = False
            mqtt_client.publish("commands/4SD", json.dumps({"stopwatch": stopwatch}))
            time.sleep(1)
            stopwatch -= 1
            
            if stopwatch == 0:
                blinking = True
                
        elif blinking:
            mqtt_client.publish("commands/4SD", json.dumps({"blink": -1}))
            time.sleep(1)
            
        else:
            time.sleep(1)

if __name__ == '__main__':
    lcd_thread = threading.Thread(target=lcd_rotation_loop)
    lcd_thread.daemon = True
    lcd_thread.start()

    stopwatch_thread = threading.Thread(target=stopwatch_background_loop)
    stopwatch_thread.daemon = True
    stopwatch_thread.start()

    app.run(debug=False)
