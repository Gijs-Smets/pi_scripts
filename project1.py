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
heat = digitalio.DigitalInOut(board.D22)
heat.direction = digitalio.Direction.OUTPUT

lock = threading.Lock()
lux          = round(light_sensor.lux, 2)
temperature  = round(pressure_sensor.temperature, 1)
target_light = 500
target_heat  = 22
duty_cycle   = 0

with lock:
    sensor_data = {
        "lux"          : lux,
        "temperature"  : temperature,
        "target_light" : target_light,
        "target_heat"  : target_heat,
    }

def publish():
    while not exit_event.is_set():
        with lock:
            lux          = sensor_data["lux"]
            temperature  = sensor_data["temperature"]
            target_light = sensor_data["target_light"]
            target_heat  = sensor_data["target_heat"]

        payload = f"field1={lux}&field2={temperature}&field3={target_light}&field4={target_heat}"
        client.publish(MQTT_TOPIC, payload)
        print(f"Published → Light: {lux} lux | Temp: {temperature}°C | Target light: {target_light} | Target heat: {target_heat}")

        exit_event.wait(timeout=15)

t1 = threading.Thread(target=publish)

t1.start()

try:
    while True:
        if not input1.value:
            target_light += 20
        if not input2.value:
            target_light -= 20
        if not input3.value:
            target_heat += 0.5
        if not input4.value:
            target_heat -= 0.5

        target_light = max(0, target_light)

        lux         = round(light_sensor.lux, 2)
        temperature = round(pressure_sensor.temperature, 1)

        with lock:
            sensor_data = {
                "lux" : lux,
                "temperature" : temperature,
                "target_light" : target_light,
                "target_heat"  : target_heat,
            }

        print(f"Light: {lux} lux | Temp: {temperature}°C | Target Light: {target_light}°C | Target Temp: {target_heat}°C")

        if duty_cycle != 0:
            if lux > target_light + 20:
                duty_cycle -= 0.1
            elif lux < target_light - 20:
                duty_cycle += 0.1
        elif lux < target_light:
            duty_cycle = 0.5
        duty_cycle = min(1, max(0, duty_cycle))

        led.duty_cycle  = int(duty_cycle * 65535)
    
        if temperature < target_heat - 0.5:
            heat.value = False
        elif temperature > target_heat + 0.5:
            heat.value = True

        time.sleep(1)

finally:
    exit_event.set()
    t1.join()
    led.duty_cycle = 0
    heat.value = True
    led.deinit()
    heat.deinit()
    client.loop_stop()
    client.disconnect()
    print("Cleaned up, exiting.")