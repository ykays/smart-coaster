import RPi.GPIO as GPIO
import logging
import itertools
import multiprocessing
import time
import queue

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
    self.display_process = None
    self.queue = None
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
    logging.info('Starting seven segment health check...')
    for char in range(10):
      start = time.time()
      while time.time() - start < 0.2:
        for digit in range(4):
          self.select_digit(digit)
          self.show_char(f'{(char + digit) % 9}')
    self.clear()

  def display_countdown(self, start_time, target_time):
    self.display_process = multiprocessing.Process(target=self._display_worker,
                                                   args=(start_time, target_time))
    self.display_process.start()

  def _display_worker(self, start_time, target_time):
    while True:
      time_remaining = target_time - (time.time() - start_time)
      display = display_time(time_remaining)
      self.display_string(display)

  def display_string(self, display):
    if len(display) != 4:
      raise ValueError(f'Can only display strings of length four: {display}')
    if any(d not in DIGIT_MAP for d in display):
      raise ValueError(f'Tried to display invalid digit(s): {display}')
    for digit in range(4):
      self.select_digit(digit)
      self.show_char(display[digit])

def display_time(time_remaining):
  seconds = int(time_remaining ) % 60
  minutes = int(time_remaining / 60) % 60
  hours = int(time_remaining / (60 * 60)) % 24
  if not hours:
    return f'{minutes:2}{seconds:02}'
  return f'{hours:2}{minutes:02}'

