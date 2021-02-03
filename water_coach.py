import itertools
import logging
import os
import time


class WaterCoach:
  def __init__(self, scale, rgb, ssegment):
    self.ssegment = ssegment
    self.scale = scale
    self.rgb = rgb
    self.reset()

  def run(self):
    self.maybe_zero_cup()
    self.prompt_target_water()
    self.prompt_target_time()
    logging.info('Drink up!')
    self.start_time = time.time()
    self.ssegment.display_countdown(self.start_time, self.target_time)
    while self.loop():
      time.sleep(0.5)  # Keep on loopin'
    self.reset()

  def reset(self):
    self.last_weight = 0
    self.start_time = None
    self.target_water = None
    self.target_time = None
    self.water_drank = 0
    self.water_added = 0
    self.rgb.set_color('WHITE')

  @property
  def water_remaining(self):
    return self.target_water - self.water_drank

  @property
  def current_time(self):
    return time.time() - self.start_time

  @property
  def is_time_done(self):
    return self.current_time > self.target_time

  @property
  def time_remaining(self):
    return self.target_time - (time.time() - self.start_time)

  def prompt_target_water(self):
    input('Place your full glass of water on the scale, then press enter.')
    self.target_water = self.scale.read_grams_high_fidelity()
    print(f'Your water goal: {self.target_water}ml')

  def prompt_target_time(self):
    self.target_time = None
    while not self.target_time:
      raw = input('What\'s your goal (in hours) for drinking the water?')
      try:
        self.target_time = float(raw) * 60 * 60
      except ValueError:
        print('I didn\'t catch that.'
              'Please enter a number of hours (such as 1.5)')

  def maybe_zero_cup(self):
    response = None
    while response not in ['y', 'n']:
      response = input(
          'Would you like to reset the weight of the glass? (y/n)')
    if response == 'y':
      self.scale.zero(
          prompt='Please place your empty cup on the scale, then press enter.')

  def check_water(self):
    new_weight = self.scale.read_grams()
    if new_weight < 0:
      return  # The user picked up the cup, ignore this.

    if new_weight > self.last_weight:
      self.water_added += new_weight - self.last_weight

    elif new_weight < self.last_weight:
      self.water_drank += self.last_weight - new_weight

    self.last_weight = new_weight

  def update_rgb(self):
    # Set light to red, yellow, or green.
    water_ratio = self.water_remaining / self.target_water
    time_ratio = self.time_remaining / self.target_time

    if (time_ratio - water_ratio) < -0.3:
      self.rgb.set_color('RED')
    elif (time_ratio - water_ratio) > 0.3:
      self.rgb.set_color('GREEN')
    else:
      self.rgb.set_color('YELLOW')

  def celebrate(self):
    for _ in itertools.repeat(50):
      for color in ['GREEN', 'TEAL', 'PURPLE']:
        self.rgb.set_color(color)
        time.sleep(0.1)

  def punish(self):
    for _ in itertools.repeat(50):
      for color in ['RED', 'BLACK']:
        self.rgb.set_color(color)
        time.sleep(0.1)

  def loop(self):
    self.check_water()
    print(f'Water drank: {self.water_drank:8}ml')
    print(f'Water added: {self.water_added:8}ml')
    print(f'Water remaining: {self.water_remaining:8}ml')

    self.update_rgb()
    if self.water_remaining <= 0:
      self.celebrate()
      return False
    if self.is_time_done:
      self.punish()
      return False
    return True
