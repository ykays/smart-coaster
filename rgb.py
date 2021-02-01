#!/usr/bin/python3
import time
import RPi.GPIO as GPIO

class Rgb:
  def __init__(self, pins):
    # Dict of {RED, GREEN, BLUE}
    GPIO.setmode(GPIO.BCM)
    self.pins = pins
    for pin in pins.values():
      GPIO.setup(pin, GPIO.OUT)
    self.cycle_leds()

  def cycle_leds(self):
    print('lighting LEDs')
    for color, pin in self.pins.items():
      print(f'Lighting: {color}')
      GPIO.output(pin, GPIO.HIGH)
      time.sleep(0.5)
      GPIO.output(pin, GPIO.LOW)
    print('Lit all colors.')
