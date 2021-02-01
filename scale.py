#!/usr/bin/python3
import collections
import statistics

from hx711 import HX711

HISTORY_SIZE = 5

class Scale:
  def __init__(self):
    self.hx711 = HX711(dout_pin=5, pd_sck_pin=6, channel='A', gain=64)
    self.reset()

  def reset(self):
    self.zero = 0
    self.hx711.reset()
    self.history = collections.deque(maxlen=HISTORY_SIZE)

  def read(self, times=10, zeroed=True, use_history=True):
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
      reading = reading - self.zero
    return reading

  def read_forever(self):
    try:
      while True:
        reading = self.read()
        print(f'Current: {reading} | History: {list(self.history)})')
    except KeyboardInterrupt:
      return

  def zero_scale(scale):
    input('Please remove all objects from the scale, then press enter.')
    print('Zeroing, please wait...')
    scale.reset()
    scale.zero = scale.read(times=10, zeroed=False)
    print(f'Zeroed to {scale.zero}!')
