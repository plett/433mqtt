# Small program to join rtl_433 to MQTT

There are many tiny scripts to take the output of rtl_433 and pipe it into
MQTT, they all push to a single topic. I have a few different 433MHz sensors
which I want to read in Home Assistant and writing Home Assistant template
rules to pull the two apart isn't fun.


## Sample input:
```
{"time" : "2018-02-17 22:11:13", "model" : "CurrentCost TX", "dev_id" : 77, "power0" : 517, "power1" : 0, "power2" : 0}
{"time" : "2018-02-17 22:11:20", "model" : "CurrentCost TX", "dev_id" : 77, "power0" : 521, "power1" : 0, "power2" : 0}
{"time" : "2018-02-17 22:11:25", "model" : "CurrentCost TX", "dev_id" : 77, "power0" : 525, "power1" : 0, "power2" : 0}
{"time" : "2018-02-17 22:11:31", "model" : "CurrentCost TX", "dev_id" : 77, "power0" : 521, "power1" : 0, "power2" : 0}
{"time" : "2018-02-17 22:11:37", "model" : "Kerui PIR Sensor", "id" : 468438, "data" : "0xa (PIR)"}
{"time" : "2018-02-17 22:11:49", "model" : "CurrentCost TX", "dev_id" : 77, "power0" : 524, "power1" : 0, "power2" : 0}
{"time" : "2018-02-17 22:11:55", "model" : "CurrentCost TX", "dev_id" : 77, "power0" : 525, "power1" : 0, "power2" : 0}
{"time" : "2018-02-17 22:12:01", "model" : "CurrentCost TX", "dev_id" : 77, "power0" : 522, "power1" : 0, "power2" : 0}
```

## Run rtl_433 and 433mqtt as:
RTL433MQTTHOST=myhost RTL433MQTTUSER=myuser RTL433MQTTPASS=mypassword rtl_433 -q -F json -U | 433mqtt.py

## Example Home Assistant config
```
sensor:
  - platform: mqtt
    state_topic: '/rtl_433/CurrentCost TX/77'
    name: 'House Power Usage'
    unit_of_measurement: 'W'
    value_template: '{{ value_json.power0 }}'
```

## TODO:
* Dedupe messages - Kerui PIR sends its message lots of times to make sure it
  gets through
