import json
from state_manager import update_state
import config
from utils import save_to_db

class AlarmSystem:
    def __init__(self, mqtt_client, influxdb_client):
        self.mqtt_client = mqtt_client
        self.influxdb_client = influxdb_client
        self.buzzer_active = False
        self.system_armed = False
        self.ALARM = False
        self.system_pin = config.SYSTEM_PIN
    
    def activate_buzzer(self, isOn):
        if not self.buzzer_active and isOn:
            self.buzzer_active = not self.buzzer_active
            self.mqtt_client.publish("commands/DB", json.dumps({"action": self.buzzer_active}))
        elif self.buzzer_active and not isOn:
            self.buzzer_active = not self.buzzer_active
            self.mqtt_client.publish("commands/DB", json.dumps({"action": self.buzzer_active}))
    
    def arm_system(self, pin):
        if int(pin) == self.system_pin:
            self.system_armed = not self.system_armed
            update_state(
                measurement="system_armed",
                name="system_armed",
                value=int(self.system_armed),
                runs_on="Server",
                simulated=True
            )
            save_to_db(self.influxdb_client, {
                "measurement": "system_armed",
                "name": "Security System",
                "value": int(self.system_armed),
                "simulated": True,
                "runs_on": "Server"
            })
            self.deactivate_alarm()
    
    def deactivate_alarm(self):
        self.ALARM = False
        self.activate_buzzer(False)
        update_state(
            measurement="ALARM",
            name="ALARM",
            value=0,
            runs_on="Server",
            simulated=True
        )
        save_to_db(self.influxdb_client, {
            "measurement": "ALARM",
            "name": "Security System",
            "value": 0,
            "simulated": True,
            "runs_on": "Server"
        })
    
    def activate_alarm(self):
        self.ALARM = True
        self.activate_buzzer(True)
        
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
        save_to_db(self.influxdb_client, payload)