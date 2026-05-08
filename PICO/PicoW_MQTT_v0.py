import os
import time
import board
import busio
import adafruit_bmp280
import ipaddress
import wifi
import socketpool
import ssl
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# Measurement settings
i2c = busio.I2C(board.GP1, board.GP0)  # uses board.SCL and board.SDA
bmp280 = adafruit_bmp280.Adafruit_BMP280_I2C(i2c, 0x77)
bmp280.sea_level_pressure = 1013.25
interval = 15 # Sample period in seconds

# MQTT settings
MQTT_HOST ="mqtt3.thingspeak.com"
MQTT_PORT = 1883
MQTT_KEEPALIVE_INTERVAL =60
MQTT_TOPIC = "channels/xxx/publish"
MQTT_CLIENT_ID = "yyy"
MQTT_USER = "yyy"
MQTT_PWD = "zzz"

# Wifi settings
WIFI_SSID = "IoTFactory"
WIFI_PASSWORD ="only4iot"
wifi.radio.connect(WIFI_SSID,WIFI_PASSWORD)
print("my IP addr:", wifi.radio.ipv4_address)
pool = socketpool.SocketPool(wifi.radio)
ssl_context = ssl.create_default_context()

def connect(mqtt_client, userdata, flags, rc):
    # This function will be called when the mqtt_client is connected
    # successfully to the broker.
    print("Connected to MQTT Broker!")
    print("Flags: {0}\n RC: {1}".format(flags, rc))


def disconnect(mqtt_client, userdata, rc):
    # This method is called when the mqtt_client disconnects
    # from the broker.
    print("Disconnected from MQTT Broker!")


def subscribe(mqtt_client, userdata, topic, granted_qos):
    # This method is called when the mqtt_client subscribes to a new feed.
    print("Subscribed to {0} with QOS level {1}".format(topic, granted_qos))


def unsubscribe(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client unsubscribes from a feed.
    print("Unsubscribed from {0} with PID {1}".format(topic, pid))


def publish(mqtt_client, userdata, topic, pid):
    # This method is called when the mqtt_client publishes data to a feed.
    print("Published to {0} with PID {1}".format(topic, pid))


def message(client, topic, message):
    print("New message on topic {0}: {1}".format(topic, message))

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=MQTT_HOST,
    port=MQTT_PORT,
    username=MQTT_USER,
    password=MQTT_PWD,
    client_id=MQTT_CLIENT_ID,
    socket_pool=pool,
    ssl_context=ssl_context,
)

# Connect callback handlers to mqtt_client
mqtt_client.on_connect = connect
mqtt_client.on_disconnect = disconnect
mqtt_client.on_subscribe = subscribe
mqtt_client.on_unsubscribe = unsubscribe
mqtt_client.on_publish = publish
mqtt_client.on_message = message

print("Attempting to connect to %s" % mqtt_client.broker)
mqtt_client.connect()


while True:
    # Print: for debugging, uncomment the following line
    print("Temperature: %4.1f, Pressure: %4.1f" % (bmp280.temperature, bmp280.pressure))
    # Create the JSON data structure
    MQTT_DATA = "field1="+str(bmp280.temperature)+"&field2="+str(bmp280.pressure)+"&status=MQTTPUBLISH"
    print(MQTT_DATA)
    try:
        mqtt_client.publish(MQTT_TOPIC, MQTT_DATA)
        time.sleep(interval)
    except OSError:
        mqtt_client.reconnect()

