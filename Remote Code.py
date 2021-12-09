"""
Remote Control code for Circuit Playground Bluefruit NeoPixel Animation and Color Remote Control.
To be used with another Circuit Playground Bluefruit running the NeoPixel Animator code.
white_led = A1
red_led = A2
blue_led = A3
green_led = TX
button = A4
"""

import board, time, touchio, digitalio, neopixel

from adafruit_circuitplayground.bluefruit import cpb
from adafruit_debouncer import Debouncer

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_bluefruit_connect.button_packet import ButtonPacket

# Set up assigive tech button on A1
button_input = digitalio.DigitalInOut(board.A4)
button_input.switch_to_input(pull=digitalio.Pull.UP)
button = Debouncer(button_input)

# Set up LEDs
white_led = digitalio.DigitalInOut(board.A1)
white_led.direction = digitalio.Direction.OUTPUT
red_led = digitalio.DigitalInOut(board.A2)
red_led.direction = digitalio.Direction.OUTPUT
blue_led = digitalio.DigitalInOut(board.A3)
blue_led.direction = digitalio.Direction.OUTPUT
green_led = digitalio.DigitalInOut(board.TX)
green_led.direction = digitalio.Direction.OUTPUT

# Flash LEDs, then set first LED to current value
lights = [white_led, red_led, blue_led, green_led]
button_selection = 0
for light in lights:
    light.value = True
time.sleep(0.25)
for light in lights:
    light.value = False
lights[button_selection].value = True

def send_packet(uart_connection_name, packet):
    """Returns False if no longer connected."""
    try:
        uart_connection_name[UARTService].write(packet.to_bytes())
    except:  # pylint: disable=bare-except
        try:
            uart_connection_name.disconnect()
        except:  # pylint: disable=bare-except
            pass
        print("No longer connected")
        return False
    return True

ble = BLERadio()
uart_server = UARTService()
advertisement = ProvideServicesAdvertisement(uart_server)
# Give your CPB a unique name between the quotes below
advertisement.complete_name = "CSremote"

# Setup for preventing repeated button presses and tracking switch state
button_a_pressed = False
button_b_pressed = False
last_switch_state = None

# setup selection list - a list of button presses to send to the receiver
button_list = [ButtonPacket.BUTTON_1, ButtonPacket.BUTTON_2, ButtonPacket.BUTTON_3, ButtonPacket.BUTTON_4, ButtonPacket.UP]

uart_connection = None
# See if any existing connections are providing UARTService.
if ble.connected:
    for connection in ble.connections:
        if UARTService in connection:
            uart_connection = connection
        break

while True:
    last_switch_state = None
    if not uart_connection or not uart_connection.connected:  # If not connected...
        print("Scanning...")
        for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):  # Scan...
            if UARTService in adv.services:  # If UARTService found...
                print("Found a UARTService advertisement.")
                print("short_name is:", adv.short_name)
                print("complete_name is:", adv.complete_name)
                if adv.complete_name == "cs-sign":
                    uart_connection = ble.connect(adv)  # Create a UART connection...
                    print("*** I just connected to cs_sign! ***")
                    if not send_packet(uart_connection,
                                   ButtonPacket(button_list[button_selection], pressed=True)):
                        print("Just sent button {}".format(button_selection))
                        uart_connection = None
                        #continue
                    break
        # Stop scanning whether or not we are connected.
        ble.stop_scan()  # And stop scanning.
    while uart_connection and uart_connection.connected:  # If connected...
        touched = False
        button.update() # checks a debounced button
        if button.fell: # if button is pressed
            print("button pressed")
            button_selection += 1
            if button_selection >= len(button_list):
                button_selection = 0
            #if light_number > len(lights):
                #light_number = 0
                print("button_selection is now", button_selection)
            for light in lights:
                light.value = False
            if button_selection < len(lights):
                lights[button_selection].value = True
            print("Option {} selected!".format(button_selection))

            if not send_packet(uart_connection,
                                   ButtonPacket(button_list[button_selection], pressed=True)):
                print("Just sent button {}".format(button_selection))
                uart_connection = None
                continue
        elif button.rose:
            pass
