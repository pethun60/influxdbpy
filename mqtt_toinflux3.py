import paho.mqtt.client as mqtt
import re
from typing import NamedTuple
from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS

token = "_Nza0Ub79pyn2hVTi4fCMkG_QvjyK68VkxyyjkKgJ8UP_R7F6raSsDFqOLezpYcKsLcpn0Xoq6BsuIH-zwwJtw=="
org = "Ptcontrol"
bucket = "Test_eldata"
MQTT_REGEX = '/el/([^/]+)/([^/]+)'
MQTT_REGEX2 = '/temperatur/([^/]+)/([^/]+)'
influxdb_client = InfluxDBClient(url="http://192.168.1.105:8086", token=token, org=org)

class SensorData(NamedTuple):
    sensor_type: str
    measurement: str
    location: str
    value: float
	
	
def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    match2 = re.match(MQTT_REGEX2, topic)
    print('test topic' + str(match))
    if match:
        sensor_type = match.group(2)
        measurement = "mqtt"
        location = match.group(1)
        print(sensor_type + '+' + location + '+' + measurement + '+' + str(payload))
        return SensorData(sensor_type, measurement, location, float(payload))
    if match2:
        sensor_type = match2.group(2)
        measurement = "mqtt"
        location = match2.group(1)
        print(sensor_type + '+' + location + '+' + measurement + '+' + str(payload))
        return SensorData(sensor_type, measurement, location, float(payload))		
    else:
        return None	
	
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" value="+str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    print('sensordata ' + str(sensor_data))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data)
	
def _send_sensor_data_to_influxdb(sensor_data):
    json_body = [
        {
            'measurement': sensor_data.measurement,
            'tags': {
                'sensor_type': sensor_data.sensor_type,
                'location': sensor_data.location
				},
            'fields': {
                'value': sensor_data.value
            }
        }
    ]
    print (json_body)
    # influxdb_client.write_points(json_body)
    write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, json_body)

client = mqtt.Client()
client.username_pw_set(username="peter", password="Peter_Th")
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.105", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
