# Import package
import paho.mqtt.client as mqtt
import ssl
import json

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
# MQTT_TOPIC = "helloTopic"
MQTT_TOPIC = "IOE7-Central-Device-Subscribe"
# MQTT_TOPIC = "IOE7-Central-Device-Publish"
MQTT_MSG = "hello MQTT"


# Group-15 Credentials
# MQTT_HOST = "a3dcijkkcxyx7s-ats.iot.us-east-1.amazonaws.com"
# CA_ROOT_CERT_FILE = "Amazon_Root_CA_1.pem"
# THING_CERT_FILE = "0b3e28ad67-certificate.pem.crt"
# THING_PRIVATE_KEY = "0b3e28ad67-private.pem.key"

# GROUP-14 Credentials
MQTT_HOST = "a2y1m4l5nyoj4c-ats.iot.us-east-2.amazonaws.com"
CA_ROOT_CERT_FILE = "./Group-14/AmazonRootCA1.pem"
THING_CERT_FILE = "./Group-14/95571a36ac-certificate.pem.crt"
THING_PRIVATE_KEY = "./Group-14/95571a36ac-private.pem.key"


# GROUP-13 Credentials
# MQTT_HOST = "a2fxqdjjnurfko-ats.iot.us-east-2.amazonaws.com"
# CA_ROOT_CERT_FILE = "./Group-13/AmazonRootCA1.pem"
# THING_CERT_FILE = "./Group-13/427d3049ad-certificate.pem.crt"
# THING_PRIVATE_KEY = "./Group-13/427d3049ad-private.pem.key"

# GROUP-11 Credentials
# MQTT_HOST = "a25gshlawby7lu-ats.iot.ap-south-1.amazonaws.com"
# CA_ROOT_CERT_FILE = "./Group-11/AmazonRootCA1.pem"
# THING_CERT_FILE = "./Group-11/65f3d674c0-certificate.pem.crt"
# THING_PRIVATE_KEY = "./Group-11/65f3d674c0-private.pem.key"


# Define on connect event function
# We shall subscribe to our Topic in this function
def on_connect(mosq, obj, rc,  properties=None):
    mqttc.subscribe(MQTT_TOPIC, 0)

# Define on_message event function. 
# This function will be invoked every time,
# a new message arrives for the subscribed topic 
def on_message(mosq, obj, msg):
    # print("Topic: " + str(msg.topic))
    # print("QoS: " + str(msg.qos))
    # print("Payload: " + str(msg.payload))

    if json.loads(msg.payload.decode())["headers"]["destination"] == "Group-15-A":
        print("Data received : ", msg.payload.decode())
    else :
        print("Not my packet")

def on_subscribe(mosq, obj, mid, granted_qos):
    print("Subscribed to Topic: " + 
	MQTT_MSG + " with QoS: " + str(granted_qos))

# Initiate MQTT Client
mqttc = mqtt.Client()

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Configure TLS Set
mqttc.tls_set(CA_ROOT_CERT_FILE, certfile=THING_CERT_FILE, keyfile=THING_PRIVATE_KEY, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)


# Connect with MQTT Broker
mqttc.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEPALIVE_INTERVAL)


# Continue monitoring the incoming messages for subscribed topic
mqttc.loop_forever()