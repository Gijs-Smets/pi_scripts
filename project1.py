import time
import board
import busio
import digitalio
import pwmio
import threading
import adafruit_bh1750
import adafruit_bmp280
import paho.mqtt.client as mqtt

exit_event = threading.Event()

THINGSPEAK_MQTT_USER   = "NTgSASYiLC4xCCU0ADsMOQk"
THINGSPEAK_CLIENT_ID   = "NTgSASYiLC4xCCU0ADsMOQk"
THINGSPEAK_MQTT_PASS   = "RS0g7Fh+G5/XFa3wS5LyLf91"

MQTT_HOST    = "mqtt3.thingspeak.com"
MQTT_TOPIC   = "channels/3289196/publish"
MQTT_PORT    = 1883

print("Connecting to ThingSpeak...")

client = mqtt.Client(client_id=THINGSPEAK_CLIENT_ID)
client.username_pw_set(THINGSPEAK_MQTT_USER, THINGSPEAK_MQTT_PASS)
client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
client.loop_start()  # runs MQTT in background thread

i2c = busio.I2C(board.SCL, board.SDA)
light_sensor    = adafruit_bh1750.BH1750(i2c)
pressure_sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, address=0x77)

lux         = round(light_sensor.lux, 2)
temperature = round(pressure_sensor.temperature, 1)
pressure    = round(pressure_sensor.pressure, 2)

led = pwmio.PWMOut(board.D12,frequency=5000,duty_cycle=0)


def publish(lux,temperature,pressure):
    while True:
        #ThingSpeak DATA
        payload = f"field1={lux}&field2={temperature}&field3={pressure}"
        result = client.publish(MQTT_TOPIC, payload)
        print(f"Published → Light: {lux} lux | Temp: {temperature}°C | Pressure: {pressure} hPa")
        
        time.sleep(15)
        if exit_event.is_set():
            break

t1 = threading.Thread(target=publish,args=(lux,temperature,pressure))

t1.start()

try:
    while True:
        lux         = round(light_sensor.lux, 2)
        temperature = round(pressure_sensor.temperature, 1)
        pressure    = round(pressure_sensor.pressure, 2)

        print(f"Light: {lux} lux | Temp: {temperature}°C | Pressure: {pressure} hPa")

        pwm = ((550 - lux)/550)*65525
        if pwm < 0:
            pwm = 0
        led.duty_cycle = pwm

        # # Build ThingSpeak DATA
        # payload = f"field1={lux}&field2={temperature}&field3={pressure}"

        # result = client.publish(MQTT_TOPIC, payload)

        # print(f"Published → Light: {lux} lux | Temp: {temperature}°C | Pressure: {pressure} hPa")

        time.sleep(1)

except KeyboardInterrupt:
    exit_event.set()