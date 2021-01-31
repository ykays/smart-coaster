#!/usr/bin/python3
import statistics
import time

from hx711 import HX711
import RPi.GPIO as GPIO

MENU_TEXT = """
What would you like to do?
1. Zero the scale.
2. Read forever.
"""


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
    return rounded -self.zero


def main():
  try:
    scale = Scale()
    while True:
      menu(scale)
  except KeyboardInterrupt:
    print('Goodbye!')
    return 0
  finally:
    GPIO.cleanup()


def menu(scale):
  choice = input(MENU_TEXT)
  if choice == '1':
    zero_scale(scale)
    return
  if choice == '2':
    read_forever(scale)
    return
  print('Invalid choice!')


def read_forever(scale):
  try:
    while True:
      print(scale.read())
  except KeyboardInterrupt:
    return


def zero_scale(scale):
  input('Please remove all objects from the scale, then press enter.')
  print('Zeroing, please wait...')
  scale.reset()
  scale.zero = scale.read(times=10, zeroed=False)
  print(f'Zeroed to {scale.zero}!')



if __name__ == "__main__":
  main()
