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
for input_index in range( 4 ):
    print( 'Analog %s : %s Volts' %( input_index,brd.analogs[input_index] ) ) 

brd.analogs.raw = True
for input_index in range( 4 ):
    print( 'Analog %s : %s of 1023' %( input_index,brd.analogs[input_index] ) ) 

print( 'Read RAW alls analogs in one shot' )
print( brd.analogs.states )

print( 'Read VOLTS alls analogs in one shot' )
brd.analogs.raw = False # Switch back to voltage conversion 
print( brd.analogs.states )

# === OptoIsolated Input ==========================
print( 'Read all OptoIsolated input' )
print( brd.inputs.states )
print( 'Read OptoIsolated input #3' )
print( brd.inputs[2] )

# === RELAIS ======================================
# Set REL1 and REL3 to ON (Python is 0 indexed)
print( 'Set relay by index' )
brd.relais[0] = True
brd.relais[2] = True
print( 'Relais[0..3] states : %s' % brd.relais.states ) 
sleep_ms( 2000 )
# switch all off
brd.relais.states = False 

print( 'one relay at the time')
for irelay in range( 4 ):
    print( '   relay %s' % (irelay+1) )
    brd.relais[irelay] = True # Switch on the relay
    sleep_ms( 1000 )
    brd.relais[irelay] = False # Switch OFF the relay
    sleep_ms( 500 )

print( 'Update all relais at once' )
brd.relais.states = [True, True, False, True]
sleep_ms( 2000 )
print( 'Switch ON all relais' )
brd.relais.states = True
sleep_ms( 2000 )
print( 'Switch OFF all relais' )
brd.relais.states = False

print( "That's the end folks")
