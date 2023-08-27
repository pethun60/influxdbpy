from datetime import datetime

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# You can generate an API token from the "API Tokens Tab" in the UI
token = "_Nza0Ub79pyn2hVTi4fCMkG_QvjyK68VkxyyjkKgJ8UP_R7F6raSsDFqOLezpYcKsLcpn0Xoq6BsuIH-zwwJtw=="
org = "Ptcontrol"
bucket = "Testbucket"

with InfluxDBClient(url="http://192.168.1.105:8086", token=token, org=org) as client:

    write_api = client.write_api(write_options=SYNCHRONOUS)
    data = "mem,host=host1 used_percent=23.43234543"
    write_api.write(bucket, org, data)

