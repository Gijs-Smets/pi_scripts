import paho.mqtt.client as mqtt

# ── CONFIG (match your Pico test script exactly) ─────────

BROKER_HOST  = "mqtt3.thingspeak.com"
BROKER_PORT    = 1883
MQTT_TOPIC   = "channels/3374837/subscribe"
MQTT_CLIENT   = "NTgSASYiLC4xCCU0ADsMOQk"
MQTT_USER   = "NTgSASYiLC4xCCU0ADsMOQk"
MQTT_PWD   = "RS0g7Fh+G5/XFa3wS5LyLf91"

# ────────────────────────────────────────────────────────

client = mqtt.Client(client_id=MQTT_CLIENT)
client.username_pw_set(MQTT_USER, MQTT_PWD)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to broker '%s'" % BROKER_HOST)
        client.subscribe(MQTT_TOPIC)
        print("Subscribed to '%s'" % MQTT_TOPIC)
        print("\nWaiting for messages... (Ctrl+C to stop)\n")
    else:
        print("Connection failed (rc=%d)" % rc)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print("Message received on '%s':" % msg.topic)
    print("  Raw payload: %s" % payload)

    # Parse the field1=value&status=... format
    fields = dict(item.split("=") for item in payload.split("&") if "=" in item)
    for key, value in fields.items():
        print("  %s = %s" % (key, value))
    print()

def on_disconnect(client, userdata, rc):
    print("Disconnected (rc=%d)" % rc)

client.on_connect    = on_connect
client.on_message    = on_message
client.on_disconnect = on_disconnect

print("Connecting to '%s'..." % BROKER_HOST)
client.connect(BROKER_HOST, BROKER_PORT)
client.loop_forever()