# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

# Basic example of setting digits on a LED segment display ported from Tony DiCola
# This example and library is meant to work with MicroPython machine.I2C API.
# License: Public Domain
from machine import I2C, Pin
from ht16k33.adafruit.segments import Seg7x4, Seg14x4
from time import sleep

# Raspberry Pico
i2c = I2C( 1, sda=Pin(6), scl=Pin(7) )

DELAY_BETWEEN_SEC = 4

# Create the LED segment class.
# This creates a 7 segment 4 character display:
display = Seg7x4(i2c, address=0x70)
# Or this creates a 14 segment alphanumeric 4 character display:
# display = Seg14x4(i2c=0x70)
# Or this creates a big 7 segment 4 character display
# display = BigSeg7x4(i2c)

print()
print("4 Digit, 7 or 14 Segment Display Demo Starting Up - Ctrl/C to Exit")
print()


try:
  while True:
    # Can just print a floating point number
    int_number = 3141
    print("Printing an integer number {0}".format(int_number))
    display.print(int_number, auto_round=True)
    sleep(DELAY_BETWEEN_SEC)
    display.fill(0)

    # Can just print a floating point number
    float_number = 29.2545
    print("Printing a floating point number {0}".format(float_number))
    display.print(float_number, decimal=2)
    sleep(DELAY_BETWEEN_SEC)
    display.fill(0)

    # Or, can print a hexadecimal value
    hex_number = 0xBEAD
    print("Printing a hexadecimal number {0}".format(hex(hex_number)))
    display.print_hex(hex_number)
    sleep(DELAY_BETWEEN_SEC)
    display.fill(0)

    if isinstance(display, Seg7x4):
      # Only for the Seg7x4 class - 7 segment, 4 digits
      time_value = '10:22'
      print("Printing a time of {0}".format(time_value))
      display.print(time_value)
      sleep(DELAY_BETWEEN_SEC)
      display.fill(0)

    # Or, can set indivdual digits / characters
    # Set the first character to '1':

    print("Setting individual digits / characters")
    display[0] = "1"
    # Set the second character to '2':
    display[1] = "2"
    # Set the third character to 'A':
    display[2] = "A"
    # Set the forth character to 'B':
    display[3] = "B"
    sleep(DELAY_BETWEEN_SEC)
    display.fill(0)

    # Or, can even set the segments to make up characters
    print("Setting digits using bitmasks")
    if isinstance(display, Seg7x4):
        # 7-segment raw digits
        display.set_digit_raw(0, 0xFF)
        display.set_digit_raw(1, 0b11111111)
        display.set_digit_raw(2, 0x79)
        display.set_digit_raw(3, 0b01111001)
    else:
        # 14-segment raw digits
        display.set_digit_raw(0, 0x2D3F)
        display.set_digit_raw(1, 0b0010110100111111)
        display.set_digit_raw(2, (0b00101101, 0b00111111))
        display.set_digit_raw(3, [0x2D, 0x3F])

    sleep(DELAY_BETWEEN_SEC)
    display.fill(0)

    # Show a looping marquee
    print("Displaying a marquee - can loop or not loop")
    display.marquee("Deadbeef 192.168.100.102... ", 0.2, loop=False)
    print()
    sleep(DELAY_BETWEEN_SEC)
    display.fill(0)
except KeyboardInterrupt:
  display.fill(0)
  print("Exiting")
