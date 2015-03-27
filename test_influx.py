#!/usr/bin/python

from influxdb import InfluxDBClient

def get_current_time():
  return int(time.time())

client = InfluxDBClient('192.168.7.3', 9086, 'root', 'root', 'demo')

json_body = [{
  "points": [get_current_time(), 9001],
  "name": "test",
  "columns": ["time", "vincents_power_level"]
}]

client.write_points(json_body)