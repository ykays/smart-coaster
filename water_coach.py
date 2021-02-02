import logging
import os
import queue

class WaterCoach:
  def __init__(self, scale, rgb, ssegment):
    self.scale = scale
    self.rgb = rgb
    self.start_time = None
    self.target_water = None
    self.target_time = None
    self.water_drank = 0
    self.water_added = 0

  def run(self):
    self.maybe_zero_cup()
    self.start_timer()
    self.queue = queue.Queue(maxsize=1)
    ssegment_thread = ssegment.display_from_queue(self.queue)
    self.loop()

  @property
  def water_remaining(self):
    return self.target_water - self.water_drank

  @property
  def is_time_done(self):
    return time.time() - self.start_time > self.target_time

  @property
  def display_time(self):
    return ' 200'

  def check_water(self):
    pass

  def update_rgb(self):
    pass

  def celebrate(self):
    pass

  def punish(self):
    pass

  def push_time(self):
    try:
      self.queue.put_nowait(self.display_time)
    except queue.Full:
      pass  # Segment didn't pick up the last one, yet.

  def loop(self):
    self.check_water()
    print(f'Water remaining: {self.water_remaining}ml')

    self.update_rgb()
    if self.water_remaining <= 0:
      self.celebrate()
    if self.is_time_done:
      self.punish()
