#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import sys
import os

host = os.environ.get('RTL433MQTTHOST')
port = int(os.environ.get('RTL433MQTTPORT', 1883))
username = os.environ.get('RTL433MQTTUSER','rtl_433')
password = os.environ.get('RTL433MQTTPASS')
topic = os.environ.get('RTL433MQTTTOPIC','/rtl_433')

#fields which might contain a device id
idfields= [
    'id', #most devices
    'dev_id', #currentcost
    'device', #ambient_weather vaillant_vrt340f
    'sensor_id', #accurite
    'node', #emontx
    'device id', #hondaremote
    'address', #ht680
    'sid' #oregon_scientific springfield
    ]

if __name__ == "__main__":
    client = mqtt.Client()
    client.username_pw_set(username,password)
    client.tls_set()
    client.connect(host,port)
    client.loop_start()
    while 1:
        try:
            line = sys.stdin.readline().rstrip()
        except KeyboardInterrupt:
            break
        if not line:
            break

        try:
            jsonline = json.loads(line)
        except ValueError:
            # this is not a valid line of json, skip it
            continue

        #find if we have a model name
        model = 'unknown'
        if 'model' in jsonline:
            model = str(jsonline['model'])

        # find if we have an id field
        idname='unknown'
        for idfield in idfields:
            if idfield in jsonline:
                idname = str(jsonline[idfield])
                break

        #print(model,'/',idname,'=', line)
        fulltopic = ''+topic+'/'+model+'/'+idname
        client.publish(fulltopic,line)

    client.loop_stop()
    client.disconnect()
