'''
modrgb is a micropython module for the Olimex MOD-RGB board. 
It allows the user to control one or more MOD-RGB board.

MOD-RGB board : http://shop.mchobby.be/product.php?id_product=1410 
MOD-RGB board : https://www.olimex.com/Products/Modules/LED/MOD-RGB/open-source-hardware  
User's guide : https://www.olimex.com/Products/Modules/LED/MOD-RGB/resources/MOD-RGB_fw_rev_3.pdf 

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

import ustruct
from machine import Pin

class MODRGB():
    """
    Class to control the MOD-RGB board.


    MODRGB.change_address( 0x22 ) : change the module address to 0x22 (instead of the default address 0x58).
                                   The "BUT" board button must be hold down while issuing the command!
    """

    def __init__( self, i2c_bus, addr=0x20 ):
        self.i2c    = i2c_bus # Initialized I2C bus 
        self.addr   = addr    # MOD-IO board address

    def pwm( self, enable ):
        """enable/disable LED PWM. 
        Enable PWM to display the color st with set_rgb(). 
        Disable PWM to switch off the strip. """
        nAck = self.i2c.writeto( self.addr, bytes([0x01 if enable else 0x02]))
        if nAck != 1:
            raise Exception( 'Invalid data size!' )

    def audio( self, enable ):
    	"""enable/disable LED Audio mode"""
    	nAck = self.i2c.writeto( self.addr, bytes([0x14 if enable else 0x15]))
    	if nAck != 1:
    		raise Exception( 'Invalid data size!')

    def set_rgb( self, color ):
        """ set the RGB color from a tuple (red,green,blue) """
        assert (type(color) is tuple) or (type(color) is list), '(r,g,b) or [r,g,b] required'
        assert len( color )==3, 'must have r,g,b items'
        assert all([0<=i<=255 for i in color]), '8 bit colors!'
        nAck = self.i2c.writeto( self.addr, bytes([0x03,color[0],color[1],color[2]]) ) # send 0x03,r,g,b
        if nAck != 4:
            raise Exception( 'Invalid data size!')

    def black(self):
        """ disable all leds. """
        self.set_rgb((0,0,0))

    def board_id( self ):
        """ return the board id """
        self.i2c.writeto( self.addr, bytes([0x20]) )
        data = self.i2c.readfrom( self.addr, 1) # read 1 bytes
        return int(data[0])

    def change_address( self, new_address ):
        """ Change the I2C address of the module. Effective immediately.

        WARNING: The "BUT" board button must be hold down while issuing the command!

        EG: MODIO.change_address( 0x22 ) """
        assert 0x8 <= new_address <= 0x77, 'Invalid I2C address!'
        nAck = self.i2c.writeto( self.addr, bytes([0xF0, new_address]) )
        # we should have exactly 2 Ack since we send 2 bytes
        if nAck != 2:
            raise Exception( 'Invalid data size!')
        # apply new address to current instance
        self.addr = new_address