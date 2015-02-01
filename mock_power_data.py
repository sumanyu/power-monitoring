#!/usr/bin/python

from influxdb import InfluxDBClient
from random import gauss
import time
from math import sin, cos, pi

off_peak_cost = 7.7
mid_peak = 11.4
on_peak = 14.0

def get_current_time():
  return int(time.time())

def bound(arg, lower, upper):
  return min(max(arg, lower), upper)

def utility_cost_for_next_hour(day, hour):
  # Weekend
  if day in [5, 6]:
    return off_peak_cost + (-2.0 * sin(pi * day / 11.0))
  else:
    if hour in range(0, 7):
      return off_peak_cost + (-2.0 * sin(pi * day / 7.0))
    elif hour in range(19, 24):
      return off_peak_cost
    elif hour in range(11, 17):
      return mid_peak
    else:
      return on_peak

# http://www.ontarioenergyboard.ca/OEB/Consumers/Electricity/Electricity+Prices
# http://www.ontarioenergyboard.ca/oeb/Consumers/Electricity/Electricity%20Prices/Historical%20Electricity%20Prices
def utility_price_model(start_time, end_time, rate=1):
  print "Starting utility_price_model..."

  # Assume starting time is fixed to be at 0 second, 0 minute of whatever hour

  current_epoch_time=start_time

  power_data = []

  while current_epoch_time < end_time:

    current_day = time.localtime(current_epoch_time).tm_wday
    current_hour = time.localtime(current_epoch_time).tm_hour

    # Get next hour's worth of price for current day
    utility_cost = utility_cost_for_next_hour(current_day, current_hour)
    utility_cost_with_noise = utility_cost + gauss(0, 0.2)

    power_data.append({
      'time': current_epoch_time,
      'cost': utility_cost_with_noise
    })

    current_epoch_time += rate

  print "Power data size: %d" % len(power_data)

  return power_data

def fridge_model(start_time, end_time, rate=1, period=20 * 60, idle_power=550, peak_power=700):
  print "Starting fridge_model..."
  period_split = gauss(0.5, 0.2)

  # Place upper and lower bounds on the proportion split between idle and busy
  period_split = bound(period_split, 0.15, 0.85)

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
      current_epoch_time+=rate

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
      current_epoch_time+=rate

  print "Power data size: %d" % len(power_data)

  return power_data

def post_data_to_influx(data, column_name, client):
  json_body = [{
      "points": data,
      "name": "power_consumption",
      "columns": ["time", column_name]
  }]

  client.write_points(json_body)

def mock_data(client):
  # Generate fake data
  start_time = 1420645462
  end_time = 1423064662

  num_iterations = 50
  iteration_period = int((end_time - start_time) / num_iterations)

  iteration_time_count = start_time

  # Slice the data into num_iterations to avoid mem overflow
  while iteration_time_count < end_time:
    _start_time = iteration_time_count
    _end_time = _start_time + iteration_period

    # print "Start time: %d" % _start_time
    # print "End time: %d" % _end_time
      # "columns": ["ts", "fridge", "tv", "lighting", "utility_cost", "washer", "dryer"]
    rate = 2

    post_data_to_influx([ [d['time'], d['p']] for d in fridge_model(_start_time, _end_time, rate = rate) ], "fridge", client)
    post_data_to_influx([ [d['time'], d['cost']] for d in utility_price_model(_start_time, _end_time, rate = rate) ], "utility_cost", client)

    # print fridge_data[0]
    # print fridge_data[1]
    # delete from power_consumption
    # drop series power_consumption

    iteration_time_count = _end_time

def main():
  print "Creating influx client..."
  client = InfluxDBClient('localhost', 8086, 'root', 'root', 'demo')
  mock_data(client)

if __name__ == '__main__':
  main()