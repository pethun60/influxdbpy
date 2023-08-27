from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "_Nza0Ub79pyn2hVTi4fCMkG_QvjyK68VkxyyjkKgJ8UP_R7F6raSsDFqOLezpYcKsLcpn0Xoq6BsuIH-zwwJtw=="
org = "Ptcontrol"
bucket = "Test_eldata"



def writetoInflux(data):
	
    with InfluxDBClient(url="http://192.168.1.105:8086", token=token, org=org) as client:

        write_api = client.write_api(write_options=SYNCHRONOUS)
        #data = "mqtt,topic=/temperatur/innetemp value=22.7"
        writeResult=write_api.write(bucket, org, data)
        client.close()
        return writeResult
		
if __name__ == '__main__':
        data = "mqtt,topic=/temperatur/innetemp value=22.7"
        data1 = "mqtt,topic=/temperatur/utetemp value=5.8"
        data2 = "mqtt,topic=/temperatur/innetemp value=23.0"
        writeInflux=writetoInflux(data)
        print("writing to influx with data ")
        writeInflux=writetoInflux(data1)
        print("writing to influx with data1 ")
        writeInflux=writetoInflux(data2)
        print("writing to influx3 with data2 ")
        print(writeInflux)