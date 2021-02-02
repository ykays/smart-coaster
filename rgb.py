#!/usr/bin/python3
import logging
import time
import RPi.GPIO as GPIO

class Rgb:
  def __init__(self, pins):
    # Dict of {RED, GREEN, BLUE}
    GPIO.setmode(GPIO.BCM)
    self.pins = pins
    for pin in pins.values():
      GPIO.setup(pin, GPIO.OUT)

  def cycle_leds(self):
    logging.info('Starting RGB health check...')
    for color, pin in self.pins.items():
      logging.info(f'Lighting: {color}')
      GPIO.output(pin, GPIO.HIGH)
      time.sleep(0.2)
      GPIO.output(pin, GPIO.LOW)
    logging.info('RGB health check complete!')
