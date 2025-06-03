# Import package
import paho.mqtt.client as mqtt
import ssl

# Define Variables
MQTT_PORT = 8883
MQTT_KEEPALIVE_INTERVAL = 45
MQTT_TOPIC = "helloTopic"
# MQTT_TOPIC = "expt7IOT"
MQTT_MSG = "hello MQTT"

MQTT_HOST = "a3dcijkkcxyx7s-ats.iot.us-east-1.amazonaws.com"
CA_ROOT_CERT_FILE = "Amazon_Root_CA_1.pem"
THING_CERT_FILE = "0b3e28ad67-certificate.pem.crt"
THING_PRIVATE_KEY = "0b3e28ad67-private.pem.key"

# Define on connect event function
# We shall subscribe to our Topic in this function
def on_connect(mosq, obj, rc,  properties=None):
    mqttc.subscribe(MQTT_TOPIC, 0)

# Define on_message event function. 
# This function will be invoked every time,
# a new message arrives for the subscribed topic 
def on_message(mosq, obj, msg):
	print("Topic: " + str(msg.topic))
	print("QoS: " + str(msg.qos))
	print("Payload: " + str(msg.payload))

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