import rgb as rgb_util
import scale as scale_util
import RPi.GPIO as GPIO

def main():
  led_pins = {
    'RED': 16,
    'GREEN': 20,
    'BLUE': 21,
  }

  try:
    scale = scale_util.Scale()
    rgb = rgb_util.Rgb(led_pins)
    while True:
      menu(scale, rgb)
  except KeyboardInterrupt:
    print('Goodbye!')
    return 0
  finally:
    GPIO.cleanup()


def menu(scale, rgb):
  menu_text = ('What would you like to do?\n'
               '1. Zero the scale.\n'
               '2. Read forever.\n'
               '3. Light led.\n')
  choice = input(menu_text)

  if choice == '1':
    scale.zero_scale()
    return
  if choice == '2':
    scale.read_forever()
    return
  if choice == '3':
    rgb.cycle_leds()
    return
  print('Invalid choice!')


if __name__ == "__main__":
  main()
