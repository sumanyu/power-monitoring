#!/usr/bin/python

from influxdb.influxdb08 import InfluxDBClient
import time

def get_current_time():
  return int(time.time())

# client = InfluxDBClient('localhost', 8086, 'root', 'root', 'demo')

# client = InfluxDBClient('10.10.10.10', 8086, 'root', 'root', 'demo')

client = InfluxDBClient('192.168.7.1', 9086, 'root', 'root', 'demo')

# print client.get_list_database()

json_body = [{
  "points": [[get_current_time(), 9001]],
  "name": "power_consumption",
  "columns": ["time", "toaster"]
}]

client.write_points(json_body)