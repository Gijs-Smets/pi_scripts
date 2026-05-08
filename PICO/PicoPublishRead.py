import ssl
import time
import wifi
import busio
import board
import socketpool
from adafruit_bus_device.i2c_device import I2CDevice
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# ── Config

WIFI_SSID     = "IoTFactory"
WIFI_PASSWORD = "only4iot"

MQTT_HOST      = "mqtt3.thingspeak.com"
MQTT_PORT      = 1883
MQTT_TOPIC     = "channels/3374837/publish"
MQTT_CLIENT_ID = "HjMVCigZHiQSBy0KMCkFNQM"
MQTT_USER      = "HjMVCigZHiQSBy0KMCkFNQM"
MQTT_PWD       = "rktxcPzv57Igr3uvyOa8hv2r"

interval = 5  # seconds

# Connection settings
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

#set up I2CDevice
sda = board.GP0
scl = board.GP1

i2c = busio.I2C(scl, sda)
device = I2CDevice(i2c, 0x23) # i2c address

with device:
        bytes_to_write = bytearray([0x10]) # 1lx resolution 120ms see datasheet
        device.write(bytes_to_write)


while True:
    #read Lux
    with device:
        bytes_read = bytearray(2)
        device.readinto(bytes_read)
    lux = (((bytes_read[0]&3)<<8) + bytes_read[1])/1.2 # conversion see datasheet
    print("%.2f Lux (no lib)" % lux)
    # Print: for debugging, uncomment the following line
    print("Test data : 420 lux")
    # Create the JSON data structure
    # MQTT_DATA = "field1="+str(bmp280.temperature)+"&field2="+str(bmp280.pressure)+"&status=MQTTPUBLISH"
    MQTT_DATA = "field1=420&status=MQTTPUBLISH"
    print(MQTT_DATA)
    try:
        mqtt_client.publish(MQTT_TOPIC, MQTT_DATA)
        time.sleep(interval)
    except OSError:
        mqtt_client.reconnect()
