import RPi.GPIO as GPIO
import itertools
import time
GPIO.setmode(GPIO.BCM)

PIN_TO_NUMBER = {
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
    self.pins = pins
    for segment in pins['SEGMENTS']:
      GPIO.setup(segment, GPIO.OUT, initial=GPIO.LOW)

    for digit in pins['DIGITS']:
      GPIO.setup(digit, GPIO.OUT, initial=GPIO.HIGH)

  def cycle_segments(self):
    print('Starting seven segment health check...')
    digits = self.pins['DIGITS']
    segments = self.pins['SEGMENTS']
    for digit, segment in itertools.product(digits, segments):
      print(f'Lighting digit {digit}, segment {segment}')
      GPIO.output(digit, GPIO.HIGH)
      GPIO.output(segment, GPIO.HIGH)
      time.sleep(0.05)
      GPIO.output(digit, GPIO.LOW)
      GPIO.output(segment, GPIO.LOW)
    print('Seven segment health check complete!')
