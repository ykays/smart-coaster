#!/usr/bin/python3
import collections
import logging
import os
import statistics

from hx711 import HX711

HISTORY_SIZE = 10
# How accurate reads must be to count them.
READ_TOLERANCE = 0.9
READ_SIZE = 3


class Scale:
  def __init__(self, data_dir):
    self.data_dir = data_dir
    self.hx711 = HX711(dout_pin=5, pd_sck_pin=6, channel='A', gain=64)
    self.reset()
    self.load_from_data()

  def reset(self):
    self.known_grams = 1
    self.calibrate_weight = 1
    self.empty_weight = 0
    self.hx711.reset()
    self.history = collections.deque(maxlen=HISTORY_SIZE)

  def get_grams(self, reading):
    return int(round(reading * self.gram_to_read_ratio))

  @property
  def calibrate_file(self):
    return os.path.join(self.data_dir, '.scale-calibrate')

  @property
  def zero_file(self):
    return os.path.join(self.data_dir, '.scale-zero')

  def load_from_data(self):
    try:
      with open(self.calibrate_file, 'r') as f:
        raw_grams, raw_weight = f.read().strip().split(',')
        self.known_grams = float(raw_grams)
        self.calibrate_weight = int(raw_weight)
        logging.info(f'Loaded ratio {self.known_grams}, {self.calibrate_weight} -> {self.gram_to_read_ratio}'
                     f' from {self.calibrate_file}')
    except (FileNotFoundError, ValueError):
      pass  # That's okay - stick with the default.

    try:
      with open(self.zero_file, 'r') as f:
        self.empty_weight = int(f.read().strip())
        logging.info(f'Zeroed to {self.empty_weight} from {self.zero_file}.')
    except (FileNotFoundError, ValueError):
      pass  # That's okay - stick with the default.

  def read(self, times=READ_SIZE, zeroed=True, use_history=True):
    reading = self.hx711.get_raw_data(times)
    reading = statistics.mean(reading)
    reading = int(round(reading, -3))
    self.history.append(reading)
    if use_history:
      reading, count = collections.Counter(self.history).most_common()[0]
      if count < (HISTORY_SIZE * READ_TOLERANCE):
        # Not very  confident in this reading - try again.
        logging.info(f'Not confident with history: {list(self.history)}')
        return self.read(times=times, zeroed=zeroed, use_history=use_history)
    if zeroed:
      reading = reading - self.empty_weight
    return reading

  def read_grams(self):
    reading = self.read()
    grams = self.get_grams(reading)
    logging.info(
        f'Current: {grams}g ({reading}) | History: {list(self.history)})')
    return grams

  def read_grams_high_fidelity(self):
    for i in range(HISTORY_SIZE):  # Build up some history.
      reading = self.read_grams()
      print(reading)
    return reading

  def read_forever(self):
    for i in range(HISTORY_SIZE):  # Build up some history.
      self.read()
    try:
      while True:
        reading = self.read()
        grams = self.get_grams(reading)
    except KeyboardInterrupt:
      return

  def zero(
      self,
      prompt='Please remove all objects from the scale, then press enter.'):
    input(prompt)
    logging.info('Zeroing, please wait...')
    self.reset()
    for i in range(HISTORY_SIZE):  # Read a bunch to eliminate flaky data.
      self.empty_weight = self.read(zeroed=False)
    with open(self.zero_file, 'w') as f:
      f.write(f'{self.empty_weight}')
    logging.info(f'Zeroed to {self.empty_weight}!')

  @property
  def gram_to_read_ratio(self):
    if self.calibrate_weight == self.empty_weight:
      raise ValueError('Must calibrate to something other than zero.')
    return self.known_grams / (self.calibrate_weight - self.empty_weight)

  def calibrate(self):
    self.known_grams = None
    while not self.known_grams:
      known_raw = input('How much weight is your known weight (in g)? ')
      try:
        self.known_grams = float(known_raw)
      except:
        logging.info('Please enter a number.')

    input(f'Please place your {self.known_grams}g object on the scale, then'
          ' press enter.')
    logging.info('Weighing, please wait...')
    for i in range(HISTORY_SIZE):  # Read a bunch to eliminate flaky data.
      self.calibrate_weight = self.read(zeroed=False)
    with open(self.calibrate_file, 'w') as f:
      f.write(f'{self.known_grams},{self.calibrate_weight}')
    logging.info(f'New ratio: {self.gram_to_read_ratio}')
