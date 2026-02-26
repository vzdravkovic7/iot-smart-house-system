import time
import json
from state_manager import get_state
import config

class StopwatchHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.stopwatch = 0
        self.blinking = False
        self.N = 0
    
    def stopwatch_background_loop(self):
        while True:
            if self.stopwatch > 0:
                self.blinking = False
                self.mqtt_client.publish("commands/4SD", json.dumps({"stopwatch": self.stopwatch}))
                time.sleep(1)
                self.stopwatch -= 1
                
                if self.stopwatch == 0:
                    self.blinking = True
                    
            elif self.blinking:
                self.mqtt_client.publish("commands/4SD", json.dumps({"blink": -1}))
                time.sleep(1)
                
            else:
                time.sleep(1)

class LCDHandler:
    def __init__(self, mqtt_client):
        self.mqtt_client = mqtt_client
        self.current_dht_index = 0
    
    def show_next_dht_on_lcd(self):
        temp_key, hum_key = config.DHT_NAMES[self.current_dht_index]

        tem = get_state(temp_key)
        hum = get_state(hum_key)

        if tem and hum:
            temperature = tem["value"]
            humidity = hum["value"]
            text = f"DHT{self.current_dht_index+1}: Temp={temperature}°C | Hum={humidity}%"
        else:
            text = f"DHT{self.current_dht_index+1}: No data"

        self.mqtt_client.publish("commands/LCD", json.dumps({"display": text}))
        self.current_dht_index = (self.current_dht_index + 1) % 3
    
    def lcd_rotation_loop(self):
        while True:
            self.show_next_dht_on_lcd()
            time.sleep(config.LCD_ROTATION_INTERVAL)