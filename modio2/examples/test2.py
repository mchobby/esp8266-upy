'''
Test the Olimex MOD-IO2 board. 

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

# === Manipulate GPIO =============================
print( "Pin_modes")
print( brd.gpios.pin_modes )

print( "GPIO 5 - Analog read")
brd.gpios.pin_mode( 5, Pin.IN )
for i in range(10):
    volt = brd.gpios.analog(5)
    print( "AN7 = %s v" % volt )
    val  = brd.gpios.analog(5, raw=True )
    print( "AN7 = %s / 1023" % val )
    sleep_ms( 1000 )

# GPIO 0 - OUT
print( "GPIO 0 - OUT (On then Off)" )
brd.gpios.pin_mode( 0, Pin.OUT )
brd.gpios[0] = True
sleep_ms( 2000 )
brd.gpios[0] = False

print( "GPIO 1,2,3 - IN" )
brd.gpios.pin_mode( 1, Pin.IN )
brd.gpios.pin_mode( 2, Pin.IN )
brd.gpios.pin_mode( 3, Pin.IN, Pin.PULL_UP ) # pull up mandatory on Pin 3
print( "Pin_modes")
print( brd.gpios.pin_modes )
print( "All inputs state (1/0)" )
print( brd.gpios.states )

# === RELAIS ======================================
# Set REL1 and REL2 to ON (Python is 0 indexed)
print( 'Set relay by index' )
brd.relais[0] = True
brd.relais[1] = False
print( 'Relais[0..1] states : %s' % brd.relais.states ) 
sleep_ms( 2000 )
# switch all off
brd.relais.states = False 

print( 'one relay at the time')
for irelay in range( 2 ):
    print( '   relay %s' % (irelay+1) )
    brd.relais[irelay] = True # Switch on the relay
    sleep_ms( 1000 )
    brd.relais[irelay] = False # Switch OFF the relay
    sleep_ms( 500 )

print( 'Update all relais at once' )
brd.relais.states = [False, True]
sleep_ms( 2000 )
print( 'Switch ON all relais' )
brd.relais.states = True
sleep_ms( 2000 )
print( 'Switch OFF all relais' )
brd.relais.states = False

print( "That's the end folks")