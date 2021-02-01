import RPi.GPIO as GPIO
import itertools
import time

DIGIT_MAP = {
    ' ': (0, 0, 0, 0, 0, 0, 0),
    '0': (1, 1, 1, 1, 1, 1, 0),
    '1': (0, 1, 1, 0, 0, 0, 0),
    '2': (1, 1, 0, 1, 1, 0, 1),
    '3': (1, 1, 1, 1, 0, 0, 1),
    '4': (0, 1, 1, 0, 0, 1, 1),
    '5': (1, 0, 1, 1, 0, 1, 1),
    '6': (1, 0, 1, 1, 1, 1, 1),
    '7': (1, 1, 1, 0, 0, 0, 0),
    '8': (1, 1, 1, 1, 1, 1, 1),
    '9': (1, 1, 1, 1, 0, 1, 1)
}


class SevenSegment:
  def __init__(self, pins):
    GPIO.setmode(GPIO.BCM)
    self.pins = pins
    for segment in pins['SEGMENTS']:
      GPIO.setup(segment, GPIO.OUT, initial=GPIO.LOW)

    for digit in pins['DIGITS']:
      GPIO.setup(digit, GPIO.OUT, initial=GPIO.HIGH)

  @property
  def segments(self):
    return self.pins.get('SEGMENTS', None)

  @property
  def digits(self):
    return self.pins.get('DIGITS', None)

  def show_char(self, char):
    values = DIGIT_MAP[char]
    for pin, value in zip(self.segments, values):
      GPIO.output(pin, value)

  def select_digit(self, new_digit):
    for segment in self.segments:
      GPIO.output(segment, GPIO.LOW)
    for digit, pin in enumerate(self.digits):
      # Ground only the pin we care about.
      GPIO.output(pin, digit != new_digit)

  def clear(self):
    for digit in self.digits:
      GPIO.output(digit, GPIO.HIGH)
    for segment in self.segments:
      GPIO.output(segment, GPIO.LOW)

  def cycle_segments(self):
    print('Starting seven segment health check...')
    for char in range(10):
      start = time.time()
      while time.time() - start < 0.2:
        for digit in range(4):
          self.select_digit(digit)
          self.show_char(str((char + digit) % 9))
    self.clear()
