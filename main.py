import rgb as rgb_util
import scale as scale_util
import ssegment as ssegment_util
import RPi.GPIO as GPIO


def setup():
  led_pins = {
      'RED': 16,
      'GREEN': 20,
      'BLUE': 21,
  }
  segment_pins = {
      'SEGMENTS': [
        11, # 7seg 11
        4,  # 7seg 7
        23, # 7seg 4
        8,  # 7seg 2
        7,  # 7seg 1
        10, # 7seg 10
        18, # 7seg 5
        25, # 7seg 3 (decimal point)
      ],
      'DIGITS': [
        22, # 1
        27, # 2
        17, # 3
        24, # 4
      ],
  }

  scale = scale_util.Scale()
  rgb = rgb_util.Rgb(led_pins)
  ssegment = ssegment_util.SevenSegment(segment_pins)

  rgb.cycle_leds()
  # ssegment.cycle_segments()
  ssegment.cycle_segments()

  return scale, rgb, ssegment


def main():
  try:
    scale, rgb, ssegment = setup()

    while True:
      menu(scale, rgb, ssegment)

  except KeyboardInterrupt:
    print('Goodbye!')
    return 0
  finally:
    GPIO.cleanup()


def menu(scale, rgb, ssegment):
  menu_text = ('What would you like to do?\n'
               '1. Zero the scale.\n'
               '2. Read forever.\n'
               '3. Test led.\n'
               '4. Test seven segment.\n'
               '(Press Ctrl-C to escape any menu)\n'
               '> ')
  choice = input(menu_text).strip()

  if choice == '1':
    scale.zero_scale()
    return
  if choice == '2':
    scale.read_forever()
    return
  if choice == '3':
    rgb.cycle_leds()
    return
  if choice == '4':
    ssegment.cycle_segments()
    return
  print('Invalid choice!')


if __name__ == "__main__":
  main()
