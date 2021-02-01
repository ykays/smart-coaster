#!/usr/bin/python3
import statistics
import time

from hx711 import HX711
import RPi.GPIO as GPIO

LED_PINS = {
  'RED': 16,
  'GREEN': 20,
  'BLUE': 21,
}


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


def main(led_pins):
  try:
    scale = Scale()
    while True:
      menu(scale, led_pins)
  except KeyboardInterrupt:
    print('Goodbye!')
    return 0
  finally:
    GPIO.cleanup()


def menu(scale, led_pins):
  menu_text = ('What would you like to do?\n'
               '1. Zero the scale.\n'
               '2. Read forever.\n'
               '3. Light led.\n')
  choice = input(menu_text)

  if choice == '1':
    zero_scale(scale)
    return
  if choice == '2':
    read_forever(scale)
    return
  if choice == '3':
    cycle_leds(led_pins)
    return
  print('Invalid choice!')


def cycle_leds(led_pins):
  print('lighting LEDs')
  for color, pin in led_pins.items():
    print(f'Lighting: {color}')
    GPIO.output(pin, GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(pin, GPIO.LOW)
  print('Lit all colors.')


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


def setup(led_pins):
  GPIO.setmode(GPIO.BCM)
  for pin in led_pins.values():
    GPIO.setup(pin, GPIO.OUT)
  cycle_leds(led_pins)


if __name__ == "__main__":
  setup(LED_PINS)
  main(LED_PINS)
