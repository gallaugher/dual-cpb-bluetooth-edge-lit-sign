# Testing Button
# White = A1
# Red = A2
# Blue = A3
# Green = TX
# Button Switch = A4

import board, neopixel, time, digitalio
from adafruit_debouncer import Debouncer

pixels_pin = board.NEOPIXEL
pixels_num_of_lights = 10
pixels = neopixel.NeoPixel(pixels_pin, pixels_num_of_lights, brightness = 0.5, auto_write=True)

white_led = digitalio.DigitalInOut(board.A1)
white_led.direction = digitalio.Direction.OUTPUT
red_led = digitalio.DigitalInOut(board.A2)
red_led.direction = digitalio.Direction.OUTPUT
blue_led = digitalio.DigitalInOut(board.A3)
blue_led.direction = digitalio.Direction.OUTPUT
green_led = digitalio.DigitalInOut(board.TX)
green_led.direction = digitalio.Direction.OUTPUT

lights = [white_led, red_led, blue_led, green_led]
light_number = 0
for light in lights:
    light.value = True
time.sleep(0.25)
for light in lights:
    light.value = False
lights[light_number].value = True

RED = (255, 0, 0)
BLACK = (0, 0, 0)

button_input = digitalio.DigitalInOut(board.A4)
button_input.switch_to_input(pull=digitalio.Pull.UP)
button = Debouncer(button_input)

while True:
    button.update() # checks a debounced button
    if button.fell: # if button is pressed
        print("button pressed")
        pixels.fill(RED)
        light_number += 1
        print(light_number, len(lights))
        if light_number > len(lights):
            light_number = 0
            print("light_number is now", light_number)
        for light in lights:
            light.value = False
        if light_number < len(lights):
            lights[light_number].value = True
        print(light_number)

    elif button.rose:
        pixels.fill(BLACK)
        # red_led.value = False

