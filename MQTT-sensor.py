import time
import board
import busio
import adafruit_bh1750
import adafruit_bmp280
import paho.mqtt.client as mqtt
import json

# ============================================================
# ThingSpeak MQTT credentials — fill these in from your account
# ============================================================
THINGSPEAK_CHANNEL_ID  = "3289196"
THINGSPEAK_MQTT_USER   = "NTgSASYiLC4xCCU0ADsMOQk"
THINGSPEAK_MQTT_PASS   = "RS0g7Fh+G5/XFa3wS5LyLf91"
THINGSPEAK_CLIENT_ID   = "NTgSASYiLC4xCCU0ADsMOQk"
THINGSPEAK_WRITE_KEY   = "LFPD7N7G6PCVFTPK"

MQTT_BROKER  = "mqtt3.thingspeak.com"
MQTT_PORT    = 1883
MQTT_TOPIC   = f"channels/{THINGSPEAK_CHANNEL_ID}/publish"

# How often to publish (ThingSpeak free tier allows 1 update per 15 seconds)
PUBLISH_INTERVAL = 15

# ============================================================
# MQTT callbacks — these run automatically on connect/disconnect
# ============================================================
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to ThingSpeak MQTT broker")
    else:
        print(f"Connection failed with code {rc}")

def on_publish(client, userdata, mid):
    print(f"Data published successfully (message id: {mid})")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Unexpected disconnection (code {rc}). Reconnecting...")
        client.reconnect()

# ============================================================
# Set up MQTT client
# ============================================================
client = mqtt.Client(client_id=THINGSPEAK_CLIENT_ID)
client.username_pw_set(THINGSPEAK_MQTT_USER, THINGSPEAK_MQTT_PASS)
client.on_connect    = on_connect
client.on_publish    = on_publish
client.on_disconnect = on_disconnect

print("Connecting to ThingSpeak...")
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()  # runs MQTT in background thread

# ============================================================
# Set up I2C sensors
# ============================================================
i2c = busio.I2C(board.SCL, board.SDA)
light_sensor    = adafruit_bh1750.BH1750(i2c)
pressure_sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)
pressure_sensor.sea_level_pressure = 1013.25

# ============================================================
# Main loop — read sensors and publish to ThingSpeak
# ============================================================
print("Starting sensor loop. Publishing every", PUBLISH_INTERVAL, "seconds...")

while True:
    try:
        # Read sensors
        lux         = round(light_sensor.lux, 2)
        temperature = round(pressure_sensor.temperature, 1)
        pressure    = round(pressure_sensor.pressure, 2)

        # Build ThingSpeak MQTT payload
        # field1 = lux, field2 = temperature, field3 = pressure
        payload = f"field1={lux}&field2={temperature}&field3={pressure}"

        # Publish
        result = client.publish(MQTT_TOPIC, payload)

        # Print to console too
        print(f"Published → Light: {lux} lux | Temp: {temperature}°C | Pressure: {pressure} hPa")

    except Exception as e:
        print(f"Error reading sensors or publishing: {e}")

    time.sleep(PUBLISH_INTERVAL)