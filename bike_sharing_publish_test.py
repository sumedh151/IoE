#!/usr/bin/python3

from __future__ import print_function
import sys
import ssl
import time
import datetime
import logging, traceback
import paho.mqtt.client as mqtt
import json
import random
import csv

IoT_protocol_name = "x-amzn-mqtt-ca"
aws_iot_endpoint = "a3dcijkkcxyx7s-ats.iot.us-east-1.amazonaws.com"
url = "https://{}".format(aws_iot_endpoint)

ca = "Amazon_Root_CA_1.pem" 
cert = "0b3e28ad67-certificate.pem.crt"
private = "0b3e28ad67-private.pem.key"

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(log_format)
logger.addHandler(handler)

def ssl_alpn():
    try:
        #debug print opnessl version
        logger.info("open ssl version:{}".format(ssl.OPENSSL_VERSION))
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)
        

        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

if __name__ == '__main__':
    # topic = "/ESP/temp"
    topic = "helloTopic"
    try:
        mqttc = mqtt.Client()
        ssl_context= ssl_alpn()
        mqttc.tls_set_context(context=ssl_context)
        logger.info("start connect")
        mqttc.connect(aws_iot_endpoint, port=443)
        logger.info("connect success")
        mqttc.loop_start()

        # while True:
        #     now = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        #     data = {
        #     "deviceId":'1',
        #     "time":now,
        #     "temp":round(random.uniform(0,100), 4),
        #     }

        #     logger.info("Publishing :{}".format(json.dumps(data)))
        #     mqttc.publish(topic, json.dumps(data))
        #     time.sleep(1)

        with open('test.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                # print(row)
                # data = {
                #     'datetime' : row[0],
                #     'season' : int(float(row[1])),
                #     'holiday' : int(float(row[2])),
                #     'workingday' : int(float(row[3])),
                #     'weather' : int(float(row[4])),
                #     'temp' : float(row[5]),
                #     'atemp' : float(row[6]),
                #     'humidity' : int(float(row[7])),
                #     'windspeed' : float(row[8]),
                #     'casual' : int(float(row[9])),
                #     'registered' : int(float(row[10])),
                #     'count' : int(float(row[11])),
                # }
                data = {
                    # "deviceId":'1',
                    'datetime' : row[0],
                    'season' : row[1],
                    'holiday' : row[2],
                    'workingday' : row[3],
                    'weather' : row[4],
                    'temp' : row[5],
                    'atemp' : row[6],
                    'humidity' : row[7],
                    'windspeed' : row[8],
                    'casual' : row[9],
                    'registered' : row[10],
                    'count' : row[11],
                }
    
                logger.info("Publishing :{}".format(json.dumps(data)))
                mqttc.publish(topic, json.dumps(data))
                time.sleep(0.01)

    except Exception as e:
        logger.error("exception main()")
        logger.error("e obj:{}".format(vars(e)))
        # logger.error("message:{}".format(e.message))
        traceback.print_exc(file=sys.stdout)
