#!/usr/bin/python

from influxdb import InfluxDBClient
from random import gauss
import time

def get_current_time():
	return int(time.time())

def bound(arg, lower, upper):
	return min(max(arg, lower), upper)

def fridge_model(period=20 * 60, idle_power=550, peak_power=700):
	period_split = gauss(0.5, 0.1)

	# Place upper and lower bounds on the proportion split between idle and busy
	period_split = bound(period_split, 0.25, 0.75)

	idle_time = period * period_split
	busy_time = period - idle_time

	power_data = []
	current_epoch_time=get_current_time()
	end_idle_epoch_time = current_epoch_time+idle_time
	end_epoch_time = end_idle_epoch_time+busy_time

	# Generate data for idling period
	while current_epoch_time < end_idle_epoch_time:
		noise = gauss(0, 20)
		power = idle_power + noise
		power_data.append({
			'ts': current_epoch_time,
			'p': power
		})
		current_epoch_time+=1

	# Generate data for thermostat period
	while current_epoch_time < end_epoch_time:
		noise = gauss(0, 20)
		power = peak_power + noise
		power_data.append({
			'ts': current_epoch_time,
			'p': power
		})
		current_epoch_time+=1

def mock_data(client):
	# Generate fake data
	json_body = [{
	    "points": [
	        ["1", 1, 1.0],
	        ["2", 2, 2.0]
	    ],
	    "name": "power_consumption",
	    "columns": ["fridge", "tv", "lighting", "utility_cost", "washer", "dryer"]
	}]
	client.write_points(json_body)

if __name__ == '__main__':
	main()

def main():
	client = InfluxDBClient('localhost', 8086, 'root', 'root', 'demo')
	mock_data(client)