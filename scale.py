#!/usr/bin/python3
import statistics

from hx711 import HX711

class Scale:
  def __init__(self):
    self.hx711 = HX711(dout_pin=5, pd_sck_pin=6, channel='A', gain=64)
    self.reset()

  def reset(self):
    self.zero = 0
    self.hx711.reset()
    self._last_readings = []

  def read(self, times=10, zeroed=True):
    readings = self.hx711.get_raw_data(times)
    mean = statistics.mean(readings)
    rounded = round(mean, -3)
    if not zeroed:
      return rounded
    return rounded - self.zero

  def read_forever(self):
    try:
      while True:
        print(self.read())
    except KeyboardInterrupt:
      return

  def zero_scale(scale):
    input('Please remove all objects from the scale, then press enter.')
    print('Zeroing, please wait...')
    scale.reset()
    scale.zero = scale.read(times=10, zeroed=False)
    print(f'Zeroed to {scale.zero}!')
