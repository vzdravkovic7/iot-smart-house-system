import json
import paho.mqtt.client as mqtt
from state_manager import update_state
import config
from utils import save_to_db

class MQTTHandler:
    def __init__(self, influxdb_client, sensor_handler, stopwatch_handler):
        self.influxdb_client = influxdb_client
        self.sensor_handler = sensor_handler
        self.stopwatch_handler = stopwatch_handler
        
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect(config.MQTT_BROKER, config.MQTT_PORT, config.MQTT_KEEPALIVE)
        self.mqtt_client.loop_start()
    
    def on_connect(self, client, userdata, flags, rc):
        for topic in config.MQTT_TOPICS:
            client.subscribe(topic)
    
    def on_message(self, client, userdata, msg):
        parsed = json.loads(msg.payload.decode('utf-8'))

        if isinstance(parsed, list):
            for data in parsed:
                self.process_data(data)
        else:
            self.process_data(parsed)
    
    def process_data(self, data):
        update_state(
            measurement=data["measurement"],
            name=data["name"],
            value=data["value"],
            runs_on=data["runs_on"],
            simulated=data["simulated"]
        )

        sensor_name = data["name"]
        value = data["value"]

        if sensor_name in ["Bedroom Infrared"]:
            self.sensor_handler.handle_bedroom_infrared(value)

        if sensor_name in ["Kitchen Button"] and value == 1:
            self.sensor_handler.handle_kitchen_button(value, self.stopwatch_handler)

        if sensor_name in ["Gyroscope Sensor_x", "Gyroscope Sensor_y", "Gyroscope Sensor_z"]:
            self.sensor_handler.handle_gsg_motion()

        if sensor_name in ["Door Membrane Switch 1"]:
            self.sensor_handler.handle_membrane_switch(value)

        if sensor_name in ["Door Motion Sensor 1", "Door Motion Sensor 2", "Living Room Motion Sensor"]:
            self.sensor_handler.handle_motion_sensors(sensor_name, value)

        if sensor_name in ["Door Sensor 1", "Door Sensor 2"]:
            self.sensor_handler.handle_door_sensors(sensor_name, value)

        save_to_db(self.influxdb_client, data)
    
    def get_client(self):
        return self.mqtt_client