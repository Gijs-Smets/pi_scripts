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

input1 = digitalio.DigitalInOut(board.D17)
input2 = digitalio.DigitalInOut(board.D27)
input3 = digitalio.DigitalInOut(board.D5)
input4 = digitalio.DigitalInOut(board.D6)

input1.direction = input2.direction = input3.direction = input4.direction = digitalio.Direction.INPUT
input1.pull = input2.pull = input3.pull = input4.pull = digitalio.Pull.UP


led  = pwmio.PWMOut(board.D12, frequency=5000, duty_cycle=0)
heat = pwmio.PWMOut(board.D13, frequency=5000, duty_cycle=0)
target_light = 0
target_heat = 500

lock = threading.Lock()
lux         = round(light_sensor.lux, 2)
temperature = round(pressure_sensor.temperature, 1)
pressure    = round(pressure_sensor.pressure, 2)

with lock:
    sensor_data = {
        "lux" : lux,
        "temperature" : temperature,
        "pressure" : pressure,
    }

def publish():
    while not exit_event.is_set():
        with lock:
            lux         = sensor_data["lux"]
            temperature = sensor_data["temperature"]
            pressure    = sensor_data["pressure"]

        payload = f"field1={lux}&field2={temperature}&field3={pressure}"
        client.publish(MQTT_TOPIC, payload)
        print(f"Published → Light: {lux} lux | Temp: {temperature}°C | Pressure: {pressure} hPa")

        exit_event.wait(timeout=15)         

t1 = threading.Thread(target=publish)

t1.start()

try:
    while True:
        if not input1.value:
            target_light += 10
        if not input2.value:
            target_light -= 10
        if not input3.value:
            target_heat += 0.1
        if not input4.value:
            target_heat -= 0.1

        lux         = round(light_sensor.lux, 2)
        temperature = round(pressure_sensor.temperature, 1)
        pressure    = round(pressure_sensor.pressure, 2)

        with lock:
            sensor_data = {
                "lux" : lux,
                "temperature" : temperature,
                "pressure" : pressure,
            }

        print(f"Light: {lux} lux | Temp: {temperature}°C | Pressure: {pressure} hPa")

        if target_light > 0:
            pwm = int(((target_light - lux) / target_light) * 65525)
            led.duty_cycle = max(0, min(65535, pwm))
        else:
            led.duty_cycle = 0

        heat.duty_cycle = int(min(65535, 65535 * target_heat))

        time.sleep(1)

finally:
    exit_event.set()
    t1.join()
    led.duty_cycle = 0
    led.deinit()
    heat.duty_cycle = 0
    heat.deinit()
    client.loop_stop()
    client.disconnect()
    print("Cleaned up, exiting.")