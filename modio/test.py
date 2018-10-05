'''
Test the Olimex MOD-IO board. 

MOD-IO board : http://shop.mchobby.be/product.php?id_product=1408 
MOD-IO board : https://www.olimex.com/Products/Modules/IO/MOD-IO/open-source-hardware  
User's guide : https://www.olimex.com/Products/Modules/IO/MOD-IO/resources/MOD-IO.pdf 

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
from modio import MODIO

i2c = I2C( sda=Pin(2), scl=Pin(4) )
brd = MODIO( i2c ) # default address=0x58

# === Read Analog Input ===========================
for irelay in range( 4 ):
    print( 'Analog %s : %s Volts' %( irelay,brd.analog(irelay) ) ) 

for irelay in range( 4 ):
    print( 'Analog %s : %s of 1023' %( irelay,brd.analog(irelay, raw=True) ) ) 

# === OptoIsolated Input ==========================
print( 'Read all OptoIsolated input' )
print( brd.inputs() )
print( 'Read OptoIsolated input #3' )
print( brd.input(2) )

# === RELAIS ======================================
# Set REL1 and REL3 to ON (Python is 0 indexed)
brd[0] = True
brd[2] = True
print( 'Relais[0..3] states : %s' % brd.relais ) 
sleep_ms( 2000 )

print( 'one relay at the time')
for irelay in range( 4 ):
    print( '   relay %s' % (irelay+1) )
    brd[irelay] = True # Switch on the relay
    sleep_ms( 1000 )
    brd[irelay] = False # Switch OFF the relay
    sleep_ms( 500 )

print( 'Update all relais at once' )
brd.relais = [True, True, False, True]
sleep_ms( 2000 )
print( 'Switch ON all relais' )
brd.relais = True
sleep_ms( 2000 )
print( 'Switch OFF all relais' )
brd.relais = False

