import time
import board
import busio
import digitalio
import adafruit_bh1750
import adafruit_bmp280
import paho.mqtt.client as mqtt

THINGSPEAK_MQTT_USER   = "NTgSASYiLC4xCCU0ADsMOQk"
THINGSPEAK_CLIENT_ID   = "NTgSASYiLC4xCCU0ADsMOQk"
THINGSPEAK_MQTT_PASS   = "RS0g7Fh+G5/XFa3wS5LyLf91"

MQTT_HOST  = "mqtt3.thingspeak.com"
MQTT_PORT    = 1883
MQTT_TOPIC   = "channels/3289196/publish"

PUBLISH_INTERVAL = 15

client = mqtt.Client(client_id=THINGSPEAK_CLIENT_ID)
client.username_pw_set(THINGSPEAK_MQTT_USER, THINGSPEAK_MQTT_PASS)

print("Connecting to ThingSpeak...")
client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
client.loop_start()  # runs MQTT in background thread

i2c = busio.I2C(board.SCL, board.SDA)
light_sensor    = adafruit_bh1750.BH1750(i2c)
pressure_sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)

D4 = digitalio.DigitalInOut(board.D4)
D4.direction = digitalio.Direction.OUTPUT

try:
    while True:
        lux         = round(light_sensor.lux, 2)
        temperature = round(pressure_sensor.temperature, 1)
        pressure    = round(pressure_sensor.pressure, 2)

        if lux > 300:
            D4.value = False
        else:
            D4.value = True

        # Build ThingSpeak DATA
        payload = f"field1={lux}&field2={temperature}&field3={pressure}"

        result = client.publish(MQTT_TOPIC, payload)

        print(f"Published → Light: {lux} lux | Temp: {temperature}°C | Pressure: {pressure} hPa")

        time.sleep(PUBLISH_INTERVAL)

finally:
    led_pwm.deinit()