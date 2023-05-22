'''
modio is a micropython module for the Olimex MOD-IO board. 
It allows the user to control one or more MOD-IO board.

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


class MIO_Digitals():
    """ Facade class to manipulate digital io """
    def __init__( self, modio_owner, io_count):
        self.count = io_count
        self.owner = modio_owner

    def __getitem__(self, index):
        """ access io state with instance[0..3] """ 
        assert index<self.count, '%s io max!' % self.count
        return self.states[index]        

    @property
    def states( self ):
        """ Get the status for ALL io. return a list """
        self.owner.i2c.writeto( self.owner.addr, bytes([0x20]) )
        data = self.owner.i2c.readfrom( self.owner.addr, 1 ) # read one byte
        return [ bool(data[0] & 0x01), bool(data[0] & 0x02), bool(data[0] & 0x04), bool(data[0] & 0x08)  ]

class MIO_Analogs():    
    """ Facade class to read analog voltage """
    def __init__( self, modio_owner, analog_count):
        self.count = analog_count
        self.owner = modio_owner
        self.raw   = False # return a voltage instead of a 10 bit range

    def __getitem__(self, index):
        """ Read an analog input (voltage or raw value) on the board.

        When returning a raw value, the method returns a value between 0 and 1023 (10 bits).
        Otherwise it returns the voltage input (between 0 and 3.3 volts). """
        assert index<self.count, '%s analog max!' % self.count
      
        # Ain1=0x30 ... Ain4=0x33
        self.owner.i2c.writeto( self.owner.addr, bytes([0x30+index]) )
        data = self.owner.i2c.readfrom( self.owner.addr, 2) # read 2 bytes
        value = ustruct.unpack( '<H', data )[0] # convert 2 bytes, LSB first to integer
        if self.raw:
            return value # 10 bits value (between 0 to 1023)
        else:
            return value * (3.3/1023) # convert to volts

    @property
    def states( self ):
        """ Get the ALL analog values. return a list.

        Do not abuse, this issue Nth exchanges on the I2C Bus """
        return list( [ self.__getitem__( index ) for index in range(self.count) ] )

class MODIO():
    """
    Class to control the MOD-IO board.

    MODIO.relais[index] = True : set the relay state.
    v = MODIO.relais[index]    : the relay state.
    MODIO.relais        : return the state of all relais.
    MODIO.relais = True : Change state of all the relais (can also use a list of 4 entries).
    MODIO.input[3]      : read an optocoupler input (True/False).
    MODIO.inputs        : read ALL optocoupler inputs (list of 4 entries)
    MODIO.analogs[3]    : read an analog input. Return a voltage.
    MODIO.analogs.raw = True: switch analog read to integer range (between 0 and 1023, 10 bit integer).

    MODIO.change_address( 0x22 ) : change the module address to 0x22 (instead of the default address 0x58).
                                   The "BUT" board button must be hold down while issuing the command!
    """

    def __init__( self, i2c_bus, addr=0x58 ):
        self.i2c    = i2c_bus # Initialized I2C bus 
        self.addr   = addr    # MOD-IO board address

        self.relais = MIO_Relais( modio_owner=self, relay_count=4 )
        # Opto isolated inputs
        self.inputs = MIO_Digitals( modio_owner=self, io_count=4 )
        # Analog read inputs
        self.analogs = MIO_Analogs( modio_owner=self, analog_count=4 )


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
