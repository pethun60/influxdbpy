from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "_Nza0Ub79pyn2hVTi4fCMkG_QvjyK68VkxyyjkKgJ8UP_R7F6raSsDFqOLezpYcKsLcpn0Xoq6BsuIH-zwwJtw=="
org = "Ptcontrol"
bucket = "Test_eldata"

with InfluxDBClient(url="http://192.168.1.105:8086", token=token, org=org) as client:

    write_api = client.write_api(write_options=SYNCHRONOUS)
    data = "mem,topic=/temperatur/innetemp value=22.7"
    write_api.write(bucket, org, data)
    data1 = "mem,topic=/temperatur/utetep value=15.0"
    write_api.write(bucket, org, data1)
    client.close()
