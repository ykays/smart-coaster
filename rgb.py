#!/usr/bin/python3
import itertools
import logging
import time
import RPi.GPIO as GPIO

COLORS = {
    'BLACK': [0, 0, 0],
    'BLUE': [0, 0, 1],
    'GREEN': [0, 1, 0],
    'PURPLE': [1, 0, 1],
    'RED': [1, 0, 0],
    'TEAL': [0, 1, 1],
    'WHITE': [1, 1, 1],
    'YELLOW': [1, 1, 0],
}


class Rgb:
  def __init__(self, pins):
    # Dict of {RED, GREEN, BLUE}
    GPIO.setmode(GPIO.BCM)
    self.pins = pins
    for pin in pins.values():
      GPIO.setup(pin, GPIO.OUT)

  def show_all_colors(self):
    logging.info('Starting color cycle...')
    for color in COLORS:
      logging.info(f'Lighting: {color}')
      self.set_color(color)
      time.sleep(1)
      for pin in self.pins.values():
        GPIO.output(pin, GPIO.LOW)
    logging.info('Color cycle complete!')

  def cycle_leds(self):
    logging.info('Starting RGB health check...')
    for color, pin in self.pins.items():
      logging.info(f'Lighting: {color}')
      GPIO.output(pin, GPIO.HIGH)
      time.sleep(0.2)
      GPIO.output(pin, GPIO.LOW)
    logging.info('RGB health check complete!')

  def set_color(self, color):
    r, g, b = COLORS[color]
    GPIO.output(self.pins['RED'], r)
    GPIO.output(self.pins['GREEN'], g)
    GPIO.output(self.pins['BLUE'], b)
