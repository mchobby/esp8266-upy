# based on https://github.com/adafruit/Adafruit_AM2315/blob/master/Adafruit_AM2315.cpp

AM2315_I2CADDR = 0x5c
AM2315_READREG = 0x03

from machine import I2C, Pin
import time
import ustruct

class AM2315:
    def __init__( self, i2c=None, addr=AM2315_I2CADDR ):
        self.addr = addr
        self.rbuf = bytearray(8) # sensor response
        if i2c != None:
            self.i2c = i2c
        else:
            # WARNING this default bus does not work 
            # on feather ESP8266 with external power supply 
            # see test.py using sda on pin 4, scl on pin 2
            self.i2c = I2C( sda=Pin(4), scl=Pin(5), freq=20000 )

    def wakeup( self ):
        # Wake up the sensor
        try: 
            self.i2c.writeto( self.addr, b'' )
            # sensor will never send ACK then OSError will ne raised
        except OSError:
            time.sleep_ms( 15 )

    def measure(self):
        self.wakeup()

        # request measure 
        wbuf = bytearray( 3 )
        wbuf[0] = AM2315_READREG
        wbuf[1] = 0x00 # Start at adress 0x00
        wbuf[2] = 0x04 # Request 4 byte data

        self.i2c.writeto( self.addr, wbuf ) # b'\x03\x00\x04' )

        # wait 1.5+ ms before reading
        time.sleep_ms( 2 )
    
        # Request 8 bytes from sensor
        #rbuf = bytearray( 8 )
        self.i2c.readfrom_mem_into(self.addr, 0, self.rbuf) # Read from Reg 0

        return self.check_response()
        
    def check_response(self):
        if self.rbuf[0] != AM2315_READREG:
            return False
        if self.rbuf[1] != 4: # Nbre bytes requested
            return False 

        # We should also check the CRC16
        # See this thread
        #  https://github.com/micropython/micropython/issues/2290

        return True

    def humidity(self):
        humidity = ( self.rbuf[2] * 256 ) + self.rbuf[3] 
        return humidity / 10

    def temperature(self):
        temp = self.rbuf[4] & 0x7F
        temp = (temp * 256) + self.rbuf[5]
        return temp / 10
