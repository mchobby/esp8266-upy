'''
modio2 is a micropython module for the Olimex MOD-IO2 board. 
It allows the user to control one or more MOD-IO2 board.

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

import ustruct
from machine import Pin

class MIO_Relais():
    """ Facade class to manipulate relais """
    def __init__( self, modio_owner, relay_count, set_relay_register = 0x10):
        self.count = relay_count
        self.owner = modio_owner
        self.__relais = 0x00    # State of all relays - all OFF 
        self.__register = set_relay_register # Relay register where to write the relay state

    def __getitem__(self, index):
        """ access relay state with instance[0..3] """ 
        assert index<self.count, '%s relais max!' % self.count
        return bool( self.__relais & (1 << index) )

    def __setitem__(self, index, value):
        assert index<self.count, '%s relais max!' % self.count
        if value:
            # activate the bit
            self.__relais = self.__relais | (0x0 | (1 << index))
        else: 
            # deactivate the bit
            self.__relais = self.__relais & (0b1111 ^ (1 << index))

        # write the relais state
        self._write_relais()

    @property 
    def states( self ):
        """ Return the relais states as a list """
        r = []
        for i in range( self.count ):
            r.append( bool(self.__relais & (1 << i) ) )
        return r

    @states.setter
    def states( self, value ):
        if type(value) is list:
            assert len(value)==self.count, "must be a list of %s values" % self.count
            for irelay in range(self.count):
                if value[irelay]:
                    # activate the bit
                    self.__relais = self.__relais | (0x0 | (1 << irelay))
                else:
                    self.__relais = self.__relais & (0b1111 ^ (1 << irelay))
        else:
            for irelay in range(self.count):
                if value:
                    # activate the bit
                    self.__relais = self.__relais | (0x0 | (1 << irelay))
                else:
                    self.__relais = self.__relais & (0b1111 ^ (1 << irelay))

        # Write all relay at once
        self._write_relais()

    @property
    def inner_state( self ):
        """ return the inner state value """
        return self.__relais

    def _write_relais( self ):
        """ send inner state to relais """
        # default relay register is 0x10
        nAck = self.owner.i2c.writeto( self.owner.addr, bytes([self.__register,self.__relais]))
        # we should have exactly 2 Ack since we send 2 bytes
        if nAck != 2:
            raise Exception( 'Invalid data size!')

class MIO2_GPIOs():
    """ MOD-IO2 has versatile I/O function like Analog input, Digital Input (with or without PullUp), PWM """
    def __init__( self, modio_owner ):
        self.owner = modio_owner
        # see the firmware readme for more informations
        self.__TRIS = 0b1111111 # current pin direction (GPIO 3 always input) 
        self.__LAT  = 0b0000000 # current level (High/Low) of GPIO (for output)
        self.__PU   = 0b0000100 # current pull-up config (GPIO 3 always pull-up)

    def pin_mode( self, gpio, pinmode, pull_up=None ):
        """ Set a given GPIO as digital I/O. pin_mode in Pin.IN, Pin.OUT, pull_up=Pin.PULL_UP/None"""
        assert gpio<7, "7 GPIOs max!"
        
        if pinmode == Pin.OUT:
            if gpio == 3:
                raise Exception( 'GPIO 3 is input only!')
            # set the corresponding bit to 0 = OUTPUT
            self.__TRIS = self.__TRIS  & ( 0b1111111 ^ (1 << gpio) )
        else:
            # set the corresponding bit to 1 = INPUT
            self.__TRIS = self.__TRIS | ( 1 << gpio )

        
        if pinmode == Pin.OUT:
        	# RESET Pull Up for output
        	# set the corresponding bit to 0 = DISABLE pull-up
            self.__PU = self.__PU & ( 0b1111111 ^ (1 << gpio) )
        else:
            # Activate Pull Up as requested for INPUT
            if pull_up == Pin.PULL_UP:
            	if not( gpio in (0,1,2,3,4) ):
            		raise Exception( 'Pull-up on %s not allowed!' % gpio )
                # set the corresponding bit to 1 = ACTIVATE pull-up
                self.__PU = self.__PU | ( 1 << gpio )  
            else:
            	# cannot disable pull-up on gpio 3
            	if gpio==3:
            		raise Exception( 'Disable Pull-up on %s not allowed' % gpio)
                # set the corresponding bit to 0 = DISABLE pull-up
                self.__PU = self.__PU & ( 0b1111111 ^ (1 << gpio) )
        
        nAck = self.owner.i2c.writeto( self.owner.addr, bytes([0x01,self.__TRIS]))
        # we should have exactly 2 Ack since we send 2 bytes
        if nAck != 2:
            raise Exception( 'Invalid data size!')
        nAck = self.owner.i2c.writeto( self.owner.addr, bytes([0x04,self.__PU]))
        # we should have exactly 2 Ack since we send 2 bytes
        if nAck != 2:
            raise Exception( 'Invalid data size!')

    @property
    def pin_modes(self):
    	""" return an array with pin modes """
    	r = []
    	for gpio in range(7):
    		r.append( 'OUT' if self.is_output(gpio) else 'IN' ) 
        return r

    def is_output( self, gpio ):
    	""" Check if a GPIO is configured as output! """
        assert gpio<7, "7 GPIOs max!" 
        return ((self.__TRIS^0b1111111) & (1<<gpio)) # __TRIS bit=0 -> output

    def __setitem__( self, gpio, value ):
        """ Set the state of a GPIO """
        if type(value) is bool:
            if not self.is_output(gpio):
                raise Exception( "gpio %s not OUTPUT mode" % gpio )
            if value:
                # set the corresponding bit to 1 = HIGH
                self.__LAT = self.__LAT | ( 1 << gpio )
            else:
                # set the corresponding bit to 0 = LOW
                self.__LAT = self.__LAT  & ( 0b1111111 ^ (1 << gpio) ) 
            
            nAck = self.owner.i2c.writeto( self.owner.addr, bytes([0x02,self.__LAT]))
            # we should have exactly 2 Ack since we send 2 bytes
            if nAck != 2:
                raise Exception( 'Invalid data size!')
            return 
        raise Exception('Invalid data type to set GPIO')

    @property
    def states( self ):
        """ Return digital states for all inputs (jit read) mix with output states.
            This should represent the real state of all the GPIO """
        nAck = self.owner.i2c.writeto( self.owner.addr, bytes([0x03]) )
        assert nAck==1
        data = self.owner.i2c.readfrom( self.owner.addr, 1) # read 1 bytes
        #print( int(data[0]) )
        r = []
        for gpio in range( 7 ):
            if self.is_output( gpio ):
                # extract state from __LAT
                r.append( bool(self.__LAT & (1<<gpio)) )
            else:
                # extract state from data
                r.append( bool(data[0] & (1<<gpio)) )
        return r


    def analog( self, gpio, raw = False ):
        """ Read a given as GPIO as Analog input. Returns voltage (3.3v max) or 10 bit integer (0-1023) in raw mode """
        assert gpio in (0,1,2,3,5), 'Analog not allowed on %s!' % gpio 
        # auto switch the gpio as input (cfr. firmware readme.txt file)
        if self.is_output( gpio ):
            # set the corresponding bit to 1 = INPUT as the microcontroler will do
            self.__TRIS = self.__TRIS | ( 1 << gpio )

        # An0=0x10 ... An6=0x15
        self.owner.i2c.writeto( self.owner.addr, bytes([0x10+gpio]) )
        data = self.owner.i2c.readfrom( self.owner.addr, 2) # read 2 bytes
        value = ustruct.unpack( '<H', data )[0] # convert 2 bytes, LSB first to integer
        if raw:
            return value # 10 bits value (between 0 to 1023)
        return value * (3.3/1023) # convert to volts

    def pwm( self, gpio, cycle ):
        """ configure the gpio as PWM output and set the duty cycle """
        assert gpio in (5,6),  'PWM not allowed on %s!' % gpio
        assert 0<= cycle <= 255, 'Invalid PWM duty cycle'

        if not self.is_output( gpio ):
            # set the corresponding bit to 0 = OUTPUT
            self.__TRIS = self.__TRIS  & ( 0b1111111 ^ (1 << gpio) )

        # GPIO 6=PWM1=0x51 ... GPIO 5=PWM2=0x52
        pwm_id = (6-gpio)+1
        self.owner.i2c.writeto( self.owner.addr, bytes([0x50+pwm_id, cycle]) )

    def pwm_close( self, gpio ):
        """ reconfigure pwm pin as input """
        assert gpio in (1,2)

        # set the corresponding bit to 1 = INPUT as the microcontroler will do
        self.__TRIS = self.__TRIS | ( 1 << gpio )
        # GPIO 6=PWM1=0x51 ... GPIO 5=PWM2=0x52
        pwm_id = (6-gpio)+1
        # CLOSE_PWM=0x50, data=1 or 2
        self.owner.i2c.writeto( self.owner.addr, bytes([0x50, pwm_id]) )

class MODIO2():
    """
    Class to control the MOD-IO2 board.
    """
    def __init__( self, i2c_bus, addr=0x21 ):
        self.i2c    = i2c_bus # Initialized I2C bus 
        self.addr   = addr    # MOD-IO board address

        self.check_version()

        self.relais = MIO_Relais( modio_owner=self, relay_count=2, set_relay_register=0x40 )
        self.gpios  = MIO2_GPIOs( modio_owner=self )

    def check_version( self ):
        """ check the board version & firmware version """
        assert self.board_id() == 0x23, "Board ID not supported"
        assert self.firmware_version() >= 64, "Require firmware version >= 64"    	

    def board_id( self ):
        """ return the board id """
        self.i2c.writeto( self.addr, bytes([0x20]) )
        data = self.i2c.readfrom( self.addr, 1) # read 1 bytes
        return int(data[0])

    def firmware_version( self ):
    	""" return the firmware version on the board """
        self.i2c.writeto( self.addr, bytes([0x21]) )
        data = self.i2c.readfrom( self.addr, 1) # read 1 bytes
        return int(data[0])

    def change_address( self, new_address ):
        """ Change the I2C address of the module. Effective immediately.

        WARNING: The "JUMPER 1" (?PROG?) must be closed while issuing the command!

        EG: MODIO2.change_address( 0x22 ) """
        assert 0x8 <= new_address <= 0x77, 'Invalid I2C address!'
        nAck = self.i2c.writeto( self.addr, bytes([0xF0, new_address]) )
        # we should have exactly 2 Ack since we send 2 bytes
        if nAck != 2:
            raise Exception( 'Invalid data size!')
        # apply new address to current instance
        self.addr = new_address