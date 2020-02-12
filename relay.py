'''
Super simple modeling of a relay for Raspberry Pi
'''

import RPi.GPIO as GPIO
#import mock_gpio as GPIO
import logging

# Force RPi to Board Pin Numbering
# - This is agnostic to Pi Model
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# Module method to cleanup all the GPIO pins
# This should be called on exit. It should only clean up the pins that
# actually get used by this program
#
# Note that if you are using other GPIO pins in your program, you should
# probably do this manually in the program.
def cleanup():
    GPIO.cleanup()

# Depending on your relay setup you may want GPIO_HIGH for "ON" or "OFF"
# By default we will set it to "ON" but provide a mechansim to switch itself.
ON = GPIO.LOW
OFF = GPIO.HIGH

def invert_relay_states():
    global OFF
    global ON
    OFF = GPIO.LOW
    ON = GPIO.HIGH
    logging.debug("Relays Inverted")

class Relay():
    # These are all the possible pins that can be used for GPIO on the RPi
    valid_gpio_pins = [3,5,7,8,10,11,12,13,15,16,18,19,21,22,23,24,26]
    def __init__(self, pin, state=False):
        self.pin = pin
        self.state = state
        if self.pin not in self.valid_gpio_pins:
            raise ValueError("Invalid GPIO pin provided : " + str(pin) +
                             "\nSupported values [" +
                             ', '.join(str(x) for x in self.valid_gpio_pins) +
                             "]")
        GPIO.setup(pin, GPIO.OUT, initial=self.state)

        if self.state == True:
            self.on()
        else:
            self.off()

    # Return the State (True if on False if off)
    def state(self):
        if self.state == OFF:
            return False
        else:
            return True

    # Set it to on
    def on(self):
        GPIO.output(self.pin, ON)
        self.state = ON
        logging.debug("Relay on pin %d ON" % self.pin)

    # Set it to off
    def off(self):
        GPIO.output(self.pin, OFF)
        self.state = OFF
        logging.debug("Relay on pin %d OFF" % self.pin)

    # Flip the state
    def toggle(self):
        logging.debug("Pre-toggle: Relay on pin %d is %s" % (self.pin, str(self.state)))
        if self.state == OFF:
            self.on()
        else:
            self.off()
        logging.debug("Post-toggle: Relay on pin %d is %s" % (self.pin, str(self.state)))
