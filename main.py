import logging
import os

import water_coach
import rgb as rgb_util
import scale as scale_util
import ssegment as ssegment_util
import RPi.GPIO as GPIO

DATA_DIR = '/home/pi/.smart-scale'


def setup():
  led_pins = {
      'RED': 16,
      'GREEN': 20,
      'BLUE': 21,
  }
  segment_pins = {
      'SEGMENTS': [
          11,  # 7seg 11
          4,  # 7seg 7
          23,  # 7seg 4
          8,  # 7seg 2
          7,  # 7seg 1
          10,  # 7seg 10
          18,  # 7seg 5
          25,  # 7seg 3 (decimal point)
      ],
      'DIGITS': [
          22,  # 1
          27,  # 2
          17,  # 3
          24,  # 4
      ],
  }

  os.makedirs(DATA_DIR, exist_ok=True)

  scale = scale_util.Scale(data_dir=DATA_DIR)
  rgb = rgb_util.Rgb(led_pins)
  ssegment = ssegment_util.SevenSegment(segment_pins)
  coach = water_coach.WaterCoach(scale, rgb, ssegment)

  return scale, rgb, ssegment, coach


def main():
  try:
    scale, rgb, ssegment, coach = setup()

    while True:
      menu(scale, rgb, ssegment, coach)

  except KeyboardInterrupt:
    print('Goodbye!')
    return 0
  finally:
    GPIO.cleanup()


def menu(scale, rgb, ssegment, coach):
  menu_text = ('What would you like to do?\n'
               '1. Calibrate the scale.\n'
               '2. Zero the scale.\n'
               '3. Read forever.\n'
               '4. Test the led.\n'
               '5. Show led colors.\n'
               '6. Test the seven segment display.\n'
               '7. Drink some water!\n'
               '(Press Ctrl-C to escape any menu)\n'
               '> ')
  choice = input(menu_text).strip()

  if choice == '1':
    scale.calibrate()
    return
  if choice == '2':
    scale.zero()
    return
  if choice == '3':
    scale.read_forever()
    return
  if choice == '4':
    rgb.cycle_leds()
    return
  if choice == '5':
    rgb.show_all_colors()
    return
  if choice == '6':
    ssegment.cycle_segments()
    return
  if choice == '7':
    coach.run()
    return
  print('Invalid choice!')


if __name__ == "__main__":
  logging.getLogger().setLevel('ERROR')
  main()
