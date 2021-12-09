# RECEIVER CODE
# e.g. code on CPB wired to the sign

import board
import neopixel
from adafruit_circuitplayground.bluefruit import cpb
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.group import AnimationGroup
from adafruit_led_animation.sequence import AnimationSequence
import adafruit_led_animation.color as color

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

import adafruit_led_animation
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowChase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.animation.SparklePulse import SparklePulse
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.sequence import AnimateOnce

from adafruit_led_animation.color import (
    AMBER, #(255, 100, 0)
    AQUA, # (50, 255, 255)
    BLACK, #OFF (0, 0, 0)
    BLUE, # (0, 0, 255)
    CYAN, # (0, 255, 255)
    GOLD, # (255, 222, 30)
    GREEN, # (0, 255, 0)
    JADE, # (0, 255, 40)
    MAGENTA, #(255, 0, 20)
    OLD_LACE, # (253, 245, 230)
    ORANGE, # (255, 40, 0)
    PINK, # (242, 90, 255)
    PURPLE, # (180, 0, 255)
    RED, # (255, 0, 0)
    TEAL, # (0, 255, 120)
    WHITE, # (255, 255, 255)
    YELLOW, # (255, 150, 0)
    RAINBOW # a list of colors to cycle through
    # RAINBOW is RED, ORANGE, YELLOW, GREEN, BLUE, and PURPLE ((255, 0, 0), (255, 40, 0), (255, 150, 0), (0, 255, 0), (0, 0, 255), (180, 0, 255))
)

runAnimation = False
animation_number = 0
lightPosition = -1

# Update to match the pin connected to your NeoPixels
led_pin = board.A1
# UPDATE NUMBER BELOW to match the number of NeoPixels you have connected
num_leds = 44
# UPDATE color below if you want your light to show a different color at startup
defaultColor = WHITE
pickedColor = defaultColor

# I've programmed these values to set, then adjust the timing of animations
defaultTime = 0.1
minWaitTime = 0.01
hundredths = 0.01
tenths = 0.1
adjustedTime = defaultTime

# Sets up the Neopixel strand,initializing it to full brightness
strip = neopixel.NeoPixel(led_pin, num_leds, pixel_order=neopixel.GRB, brightness=0.5, auto_write=True)
strip.fill((0, 0, 0))
strip.write()

# Comet animation has a dimming tail - sets the tail length
cometTailLength = int(num_leds/2) + 1

# Set LEDs to light up sold in the default color
strip.fill(pickedColor)
strip.write()

# Setup BLE connection
ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
# Give your CPB a unique name between the quotes below
advertisement.complete_name = "cs-sign"

animation_color = None
mode = 0
blanked = False

rainbowAnimation = Rainbow(strip, speed=0.05, period=2)
animations = AnimateOnce(rainbowAnimation)

# The function runSelected will run the animation number stored in the value animation_number.
# This function is called in the while True: loop whenever an animation has been started, in while not ble.connected (when not connected to bluetooth)
# or while ble.connected (when connected to bluetooth). We call it in both locations so that if
# animations are started, then the user shuts off their phone or moves out of bluetooth range, the
# last selected animation will continue to run.
def runSelectedAnimation():
    if animation_number == 0:
        strip.fill(WHITE)
        strip.write()
    elif animation_number == 1:
        strip.fill(RED)
        strip.write()
    elif animation_number == 2:
        strip.fill(BLUE)
        strip.write()
    elif animation_number == 3:
        rainbowAnimation = Rainbow(strip, speed=0.05, period=2)
        animations = AnimateOnce(rainbowAnimation)
        while animations.animate():
            animations.animate()
            #pass
        strip.fill((125, 125, 0))
        strip.write()
    elif animation_number == 4:
        strip.fill(BLACK)
        strip.write()

while True:
    ble.start_advertising(advertisement)  # Start advertising.
    was_connected = False
    while not was_connected or ble.connected:
        #if not blanked:  # If LED-off signal is not being sent...
            #pass
            #animations.animate()  # Run the animations.
        if ble.connected:  # If BLE is connected...
            was_connected = True
            if uart.in_waiting:  # Check to see if any data is available from the Remote Control.
                try:
                    packet = Packet.from_stream(uart)  # Create the packet object.
                except ValueError:
                    continue
                if isinstance(packet, ButtonPacket):  # If the packet is a button packet...
                    # Check to see if it's BUTTON_1 (which is being sent by the slide switch)
                    if packet.pressed:  # If the buttons on the Remote Control are pressed...
                        if packet.button == ButtonPacket.BUTTON_1:  # If button A is pressed...
                            print("BUTTON_1 was pressed - Animation 0")
                            animation_number = 0
                            runAnimation = True
                        if packet.button == ButtonPacket.BUTTON_2:  # If button A is pressed...
                            print("BUTTON_2 Pressed -  - Animation 1")
                            animation_number = 1
                            runAnimation = True
                        if packet.button == ButtonPacket.BUTTON_3:  # If button A is pressed...
                            print("BUTTON_3 Pressed - Animation 2")
                            animation_number = 2
                            runAnimation = True
                        if packet.button == ButtonPacket.BUTTON_4:  # If button A is pressed...
                            print("BUTTON_4 Pressed - Animation 3")
                            animation_number = 3
                            runAnimation = True
                        if packet.button == ButtonPacket.UP:  # If button A is pressed...
                            print("UP was pressed - Animation 4")
                            animation_number = 4
                            runAnimation = True
        if runAnimation == True:
            runSelectedAnimation()
    # If we got here, we lost the connection. Go up to the top and start
    # advertising again and waiting for a connection.
