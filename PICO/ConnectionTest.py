import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# ── CONFIG (match your main script exactly) ──────────────
WIFI_SSID     = "IoTFactory"
WIFI_PASSWORD = "only4iot"

MQTT_HOST      = "mqtt3.thingspeak.com"
MQTT_PORT      = 1883
MQTT_TOPIC     = "channels/3374837/publish"
MQTT_CLIENT_ID = "HjMVCigZHiQSBy0KMCkFNQM"
MQTT_USER      = "HjMVCigZHiQSBy0KMCkFNQM"
MQTT_PWD       = "rktxcPzv57Igr3uvyOa8hv2r"
# ────────────────────────────────────────────────────────

print("=" * 40)
print("MQTT CONNECTION TEST")
print("=" * 40)

# ── STEP 1: WiFi ─────────────────────────────────────────
print("\n[1/3] Connecting to WiFi '%s'..." % WIFI_SSID)
try:
    wifi.radio.connect(WIFI_SSID, WIFI_PASSWORD)
    print("      OK — IP: %s" % wifi.radio.ipv4_address)
except Exception as e:
    print("      FAILED: %s" % e)
    raise

pool = socketpool.SocketPool(wifi.radio)

# ── STEP 2: MQTT connect ──────────────────────────────────
def on_connect(client, userdata, flags, rc):
    print("      OK — Connected (rc=%d)" % rc)

def on_disconnect(client, userdata, rc):
    print("      Disconnected (rc=%d)" % rc)

def on_publish(client, userdata, topic, pid):
    print("      OK — Published to '%s' (pid=%d)" % (topic, pid))

mqtt_client = MQTT.MQTT(
    broker      = MQTT_HOST,
    port        = MQTT_PORT,
    username    = MQTT_USER,
    password    = MQTT_PWD,
    client_id   = MQTT_CLIENT_ID,
    socket_pool = pool,
)

mqtt_client.on_connect    = on_connect
mqtt_client.on_disconnect = on_disconnect
mqtt_client.on_publish    = on_publish

print("\n[2/3] Connecting to MQTT broker '%s'..." % MQTT_HOST)
try:
    mqtt_client.connect()
except Exception as e:
    print("      FAILED: %s" % e)
    raise

# ── STEP 3: Publish test message ──────────────────────────
print("\n[3/3] Publishing test message...")
TEST_PAYLOAD = "field1=69&status=HelloWorld"
try:
    mqtt_client.publish(MQTT_TOPIC, TEST_PAYLOAD)
except Exception as e:
    print("      FAILED: %s" % e)
    raise

# ── DONE ──────────────────────────────────────────────────
mqtt_client.disconnect()
print("\n" + "=" * 40)
print("ALL TESTS PASSED")
print("=" * 40)