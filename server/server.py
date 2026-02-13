from state_manager import update_state, get_all_state, get_state
from flask import Flask, jsonify, request
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import paho.mqtt.client as mqtt
import json
from flask_cors import CORS

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
    client.subscribe("DPIR3")
    client.subscribe("4SD")

mqtt_client.on_connect = on_connect

def on_message(client, userdata, msg):
    parsed = json.loads(msg.payload.decode('utf-8'))

    if isinstance(parsed, list):
        for data in parsed:
            process_data(data)
    else:
        process_data(parsed)

def process_data(data):
    update_state(
        measurement=data["measurement"],
        name=data["name"],
        value=data["value"],
        runs_on=data["runs_on"],
        simulated=data["simulated"]
    )

    save_to_db(data)

mqtt_client.on_message = on_message

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

@app.route("/api/state/<name>", methods=["GET"])
def api_device_state(name):
    result = get_state(name)
    if result is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
