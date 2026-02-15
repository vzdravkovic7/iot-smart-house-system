INFLUXDB_TOKEN = "9j45ZmqnOGoSx4XKPadoMPyot0zsX0DwZg3FpvuaDpKDFIuBomlqMCYTyT_CdRiTBjtijnb9qJXw8-9XIrH9zg=="
INFLUXDB_ORG = "FTN"
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_BUCKET = "example_db"

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_KEEPALIVE = 60

MQTT_TOPICS = [
    "Button",
    "DS2",
    "BTN",
    "PIR",
    "PIR2",
    "Ultrasonic",
    "Ultrasonic2",
    "Membrane",
    "DHT3",
    "GSG",
    "WEBC",
    "DL",
    "DB",
    "DHT1",
    "DHT2",
    "IR",
    "LCD",
    "DPIR3",
    "4SD"
]

SYSTEM_PIN = 1312
GSG_THRESHOLD = 3.0
DOOR_ALARM_DELAY = 5.0
LED_AUTO_OFF_DELAY = 10.0
MEMBRANE_ARM_DELAY = 2.0
LCD_ROTATION_INTERVAL = 4

DHT_NAMES = [
    ("Bedroom DHT_temperature", "Bedroom DHT_humidity"),
    ("Master Bedroom DHT_temperature", "Master Bedroom DHT_humidity"),
    ("Kitchen DHT Sensor_temperature", "Kitchen DHT Sensor_humidity")
]

CORS_ORIGINS = "*"