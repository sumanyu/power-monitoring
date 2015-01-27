#!/usr/bin/python

from influxdb import InfluxDBClient
from random import gauss
import time

def get_current_time():
	return int(time.time())

def bound(arg, lower, upper):
	return min(max(arg, lower), upper)

def fridge_model(start_time, end_time, period=20 * 60, idle_power=550, peak_power=700):
	print "Starting fridge_model..."
	period_split = gauss(0.5, 0.1)

	# Place upper and lower bounds on the proportion split between idle and busy
	period_split = bound(period_split, 0.25, 0.75)

	idle_time = period * period_split
	busy_time = period - idle_time

	power_data = []
	current_epoch_time=start_time

	while current_epoch_time < end_time:
		end_idle_epoch_time = current_epoch_time+idle_time
		end_epoch_time = end_idle_epoch_time+busy_time

		# print "Generating data for idling period..."
		# print "current_epoch_time: %d" % current_epoch_time
		# print "end_idle_epoch_time: %d" % end_idle_epoch_time

		# Generate data for idling period
		while current_epoch_time < end_idle_epoch_time:
			noise = gauss(0, 20)
			power = idle_power + noise
			power_data.append({
				'time': current_epoch_time,
				'p': power
			})
			current_epoch_time+=1

		# print "Generating data for busy period..."
		# print "current_epoch_time: %d" % current_epoch_time
		# print "end_epoch_time: %d" % end_epoch_time
			
		# Generate data for thermostat period
		while current_epoch_time < end_epoch_time:
			noise = gauss(0, 20)
			power = peak_power + noise
			power_data.append({
				'time': current_epoch_time,
				'p': power
			})
			current_epoch_time+=1

	print "Power data size: %d" % len(power_data)

	return power_data

def mock_data(client):
	# Generate fake data
	start_time = 1421768662
	end_time = 1422373462
	fridge_data = [ [d['time'], d['p']] for d in fridge_model(start_time, end_time) ]

	print fridge_data[0]
	print fridge_data[1]
	# delete from power_consumption
	# drop series power_consumption

	json_body = [{
	    "points": fridge_data,
	    "name": "power_consumption",
	    "columns": ["time", "fridge"]
	    # "columns": ["ts", "fridge", "tv", "lighting", "utility_cost", "washer", "dryer"]
	}]
	client.write_points(json_body)

def main():
	print "Creating influx client..."
	client = InfluxDBClient('localhost', 8086, 'root', 'root', 'demo')
	mock_data(client)

if __name__ == '__main__':
	main()