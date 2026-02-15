import json
import threading
import math
from state_manager import get_state
import config
from utils import save_people_count

class SensorHandler:
    def __init__(self, mqtt_client, influxdb_client, alarm_system):
        self.mqtt_client = mqtt_client
        self.influxdb_client = influxdb_client
        self.alarm_system = alarm_system
        
        self.last_dus1_value = None
        self.last_dus2_value = None
        self.LED_active = False
        self.people_count = 0
        self.door_timers = {}
        self.last_gsg_magnitude = None
        self.gsg_threshold = config.GSG_THRESHOLD
    
    def handle_bedroom_infrared(self, value):
        self.mqtt_client.publish("commands/BRGB", json.dumps({"action": value}))
    
    def handle_kitchen_button(self, value, stopwatch_handler):
        if value == 1:
            if stopwatch_handler.blinking:
                stopwatch_handler.blinking = False
                self.mqtt_client.publish("commands/4SD", json.dumps({"stopwatch": 0}))
            else:
                stopwatch_handler.stopwatch += stopwatch_handler.N
    
    def handle_gsg_motion(self):
        gx = get_state("Gyroscope Sensor_x")
        gy = get_state("Gyroscope Sensor_y")
        gz = get_state("Gyroscope Sensor_z")

        if not gx or not gy or not gz:
            return

        x = gx["value"]
        y = gy["value"]
        z = gz["value"]

        magnitude = math.sqrt(x*x + y*y + z*z)

        if self.last_gsg_magnitude is None:
            self.last_gsg_magnitude = magnitude
            return

        diff = abs(magnitude - self.last_gsg_magnitude)
        self.last_gsg_magnitude = magnitude

        if diff > self.gsg_threshold:
            self.alarm_system.activate_alarm()
    
    def handle_membrane_switch(self, value):
        timer = threading.Timer(config.MEMBRANE_ARM_DELAY, self.alarm_system.arm_system, args=(value,))
        timer.start()
    
    def handle_motion_sensors(self, sensor_name, value):
        if value == 1 and self.people_count == 0:
            self.alarm_system.activate_alarm()
        
        if sensor_name in ["Door Motion Sensor 1", "Door Motion Sensor 2"] and value == 1:
            self._handle_door_motion()
    
    def _handle_door_motion(self):
        dus_state1 = get_state("Door Ultrasonic Sensor 1")
        dus_state2 = get_state("Door Ultrasonic Sensor 2")

        if not self.LED_active:
            self.LED_active = not self.LED_active
            self.mqtt_client.publish("commands/DL", json.dumps({"action": "ON"}))
            timer = threading.Timer(config.LED_AUTO_OFF_DELAY, self.led_off)
            timer.start()

        if dus_state1 and self.last_dus1_value is not None:
            current_dist = dus_state1['value']
            
            if self.last_dus1_value > current_dist + 10:
                self.people_count += 1
                save_people_count(self.influxdb_client, self.people_count)
            elif self.last_dus1_value < current_dist - 10:
                self.people_count = max(0, self.people_count - 1)
                save_people_count(self.influxdb_client, self.people_count)

        if dus_state1:
            self.last_dus1_value = dus_state1['value']

        if dus_state2 and self.last_dus2_value is not None:
            current_dist = dus_state2['value']
            
            if self.last_dus2_value > current_dist + 10:
                self.people_count += 1
                save_people_count(self.influxdb_client, self.people_count)
            elif self.last_dus2_value < current_dist - 10:
                self.people_count = max(0, self.people_count - 1)
                save_people_count(self.influxdb_client, self.people_count)

        if dus_state2:
            self.last_dus2_value = dus_state2['value']
    
    def led_off(self):
        self.LED_active = not self.LED_active
        self.mqtt_client.publish("commands/DL", json.dumps({"action": "OFF"}))
    
    def handle_door_sensors(self, sensor_name, door_open):
        if door_open == 1:
            if self.alarm_system.system_armed:
                self.alarm_system.activate_alarm()
            elif sensor_name not in self.door_timers or not self.door_timers[sensor_name].is_alive():
                t = threading.Timer(config.DOOR_ALARM_DELAY, self.alarm_system.activate_alarm)
                self.door_timers[sensor_name] = t
                t.start()
        else:
            if sensor_name in self.door_timers:
                self.door_timers[sensor_name].cancel()
                del self.door_timers[sensor_name]
            
            if self.alarm_system.ALARM and not self.alarm_system.system_armed:
                self.alarm_system.deactivate_alarm()