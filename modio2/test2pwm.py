'''
Test the PWM feature of Olimex MOD-IO2 board. 
PWM is only available in GPIO 1 & 2.

Get Analog value on GPIO 5 and apply it as PWM to GPIO 1.

MOD-IO2 board : http://shop.mchobby.be/product.php?id_product=1403 
MOD-IO2 board : https://www.olimex.com/Products/Modules/IO/MOD-IO2/open-source-hardware 
User's guide : https://www.olimex.com/Products/Modules/IO/MOD-IO2/resources/MOD-IO2.pdf

The MIT License (MIT)
Copyright (c) 2018 Dominique Meurisse, support@mchobby.be, shop.mchobby.be

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''
from machine import I2C, Pin
from time import sleep_ms
from modio2 import MODIO2

i2c = I2C( sda=Pin(2), scl=Pin(4) )
brd = MODIO2( i2c ) # default address=0x21

print( "GPIO 5 - IN")
brd.gpios.pin_mode( 5, Pin.IN )

print( "GPIO 6 - PWM" )
brd.gpios.pwm( gpio=6, cycle=0 )

cycle=0
while cycle<255:
    val = brd.gpios.analog( 5, raw = True )
    cycle = val // 4 # from 0..1023 to 0..254
    if cycle >= 254: # ensure a 100% duty cycle
        cycle = 255
    brd.gpios.pwm( 6, cycle )
    print( "val=%s -> cycle=%s" %(val,cycle) )
    sleep_ms( 1000 )

print( "That's the end folks")
