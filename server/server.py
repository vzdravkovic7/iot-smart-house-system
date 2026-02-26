import json
import config
import threading
from flask import Flask, jsonify, request
from flask_cors import CORS
from influxdb_client import InfluxDBClient
from state_manager import get_all_state, get_state
from utils import handle_influx_query
from alarm_system import AlarmSystem
from sensor_handlers import SensorHandler
from background_tasks import LCDHandler, StopwatchHandler
from mqtt_handler import MQTTHandler

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": config.CORS_ORIGINS}})

influxdb_client = InfluxDBClient(
    url=config.INFLUXDB_URL,
    token=config.INFLUXDB_TOKEN,
    org=config.INFLUXDB_ORG
)

stopwatch_handler = StopwatchHandler(None)
lcd_handler = LCDHandler(None)

alarm_system = AlarmSystem(None, influxdb_client)

sensor_handler = SensorHandler(None, influxdb_client, alarm_system)

mqtt_handler = MQTTHandler(influxdb_client, sensor_handler, stopwatch_handler)
mqtt_client = mqtt_handler.get_client()

alarm_system.mqtt_client = mqtt_client
sensor_handler.mqtt_client = mqtt_client
stopwatch_handler.mqtt_client = mqtt_client
lcd_handler.mqtt_client = mqtt_client

@app.route('/store_data', methods=['POST'])
def store_data():
    try:
        data = request.get_json()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/simple_query', methods=['GET'])
def retrieve_simple_data():
    query = f"""from(bucket: "{config.INFLUXDB_BUCKET}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Button")"""
    return handle_influx_query(influxdb_client, query)

@app.route('/aggregate_query', methods=['GET'])
def retrieve_aggregate_data():
    query = f"""from(bucket: "{config.INFLUXDB_BUCKET}")
    |> range(start: -10m)
    |> filter(fn: (r) => r._measurement == "Button")
    |> mean()"""
    return handle_influx_query(influxdb_client, query)

@app.route("/api/state", methods=["GET"])
def api_all_state():
    return jsonify(get_all_state())

@app.route("/api/state/<name>", methods=["GET"])
def api_device_state(name):
    result = get_state(name)
    if result is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(result)

@app.route("/api/alarm", methods=["GET"])
def switch_alarm():
    if alarm_system.ALARM:
        alarm_system.deactivate_alarm()
    else:
        alarm_system.activate_alarm()
    return jsonify(True)

@app.route("/api/system", methods=["GET"])
def switch_system():
    alarm_system.arm_system(config.SYSTEM_PIN)
    return jsonify(True)

@app.route("/api/stopwatch", methods=["POST"])
def updateStopwatch():
    stopwatch_handler.N = int(request.json['stopwatch'])
    return jsonify(True)

@app.route("/api/brgb", methods=["POST"])
def updateBRGB():
    mode = int(request.json['action'])
    mqtt_client.publish("commands/BRGB", json.dumps({"action": mode}))
    return jsonify(True)

if __name__ == '__main__':
    lcd_thread = threading.Thread(target=lcd_handler.lcd_rotation_loop)
    lcd_thread.daemon = True
    lcd_thread.start()

    stopwatch_thread = threading.Thread(target=stopwatch_handler.stopwatch_background_loop)
    stopwatch_thread.daemon = True
    stopwatch_thread.start()

    app.run(debug=False)