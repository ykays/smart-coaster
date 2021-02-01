#!/usr/bin/python3
import collections
import statistics

from hx711 import HX711

HISTORY_SIZE = 10
READ_SIZE = 3


class Scale:
  def __init__(self):
    self.gram_to_read_ratio = 1
    self.hx711 = HX711(dout_pin=5, pd_sck_pin=6, channel='A', gain=64)
    self.reset()

  def reset(self):
    self.empty_weight = 0
    self.hx711.reset()
    self.history = collections.deque(maxlen=HISTORY_SIZE)

  def get_grams(self, reading):
    return int(round((reading + self.empty_weight) * self.gram_to_read_ratio))

  def read(self, times=READ_SIZE, zeroed=True, use_history=True):
    reading = self.hx711.get_raw_data(times)
    reading = statistics.mean(reading)
    reading = int(round(reading, -3))
    self.history.append(reading)
    if use_history:
      try:
        reading = statistics.mode(self.history)
      except statistics.StatisticsError:
        # There is no mode - get the last value, instead.
        return self.history[-1]
    if zeroed:
      reading = reading - self.empty_weight
    return reading

  def read_forever(self):
    for i in range(HISTORY_SIZE):  # Build up some history.
      self.read()
    try:
      while True:
        reading = self.read()
        grams = self.get_grams(reading)
        print(f'Current: {grams}g ({reading}) | History: {list(self.history)})')
    except KeyboardInterrupt:
      return

  def zero(self):
    input('Please remove all objects from the scale, then press enter.')
    print('Zeroing, please wait...')
    self.reset()
    for i in range(HISTORY_SIZE):  # Read a bunch to eliminate flaky data.
      self.empty_weight = self.read(times=10, zeroed=False)
    print(f'Zeroed to {self.empty_weight}!')

  def calibrate(self):
    self.zero()
    known_grams = None
    while not known_grams:
      known_raw = input('How much weight is your known weight (in g)? ')
      try:
        known_grams = float(known_raw)
      except:
        print('Please enter a number.')

    input(f'Please place your {known_grams}g object on the scale, then press enter.')
    print('Weighing, please wait...')
    for i in range(HISTORY_SIZE):  # Read a bunch to eliminate flaky data.
      read_weight = self.read(times=10, zeroed=False)
    self.gram_to_read_ratio = known_grams / read_weight
    print(f'New ratio: {self.gram_to_read_ratio}')
