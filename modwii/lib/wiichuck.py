'''
wiichuck is a micropython module for the Olimex MOD-Wii-UEXT-NUNCHUCK board.

It allows to read the status of WiiChuck game joystick.

MOD-Wii-UEXT-NUNCHUCK : http://shop.mchobby.be/product.php?id_product=1416 
MOD-Wii-UEXT-NUNCHUCK : https://www.olimex.com/Products/Modules/Sensors/MOD-WII/MOD-Wii-UEXT-NUNCHUCK/  

Based on:
  https://github.com/OLIMEX/UEXT-MODULES/blob/master/MOD-Wii-UEXT-NUNCHUCK/ARDUINO%20EXAMPLES/WII-READ/WiiChuck.h
  Please - read the comments about library precision

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
from time import sleep
from math import atan2, acos

ZEROX  = 510  
ZEROY  = 490
ZEROZ  = 460
RADIUS = 210  # probably pretty universal

DEFAULT_ZERO_JOY_X = 124
DEFAULT_ZERO_JOY_Y = 132

class WiiChuck():
    # == Private ==
    # values for the center position
    __zeroJoyX   = DEFAULT_ZERO_JOY_X  # 
    __zeroJoyY   = DEFAULT_ZERO_JOY_X  # use calibrateJoy when the stick is at zero to correct
    __joy_thres      = 60 # Thresold use then converting joystick reading to up/down/left/right 
    __joy_min_thres  = 3  # Min Mov Thresold to detect joystick movement 

    __lastJoyX, __lastJoyY = 0,0 # Correspond to last joytick position
    __angles     = [None] * 3
    __lastZ, __lastC       = 0,0 # Correspond to last button state	

    # == Protected ==
    # What as just been read from the sensor with update()
    _joyX, _joyY = 0,0
    _buttonZ, _buttonC = False, False
    _countZ, _countC = 0, 0 # Number of Button Pression count since last reading on c_count, z_count

    def __init__( self, i2c_bus, addr=0x52 ):
        self.i2c    = i2c_bus # Initialized I2C bus 
        self.addr   = addr    # WiiChuck address

        self.i2c.writeto( self.addr, bytes([0xF0, 0x55]) )
        sleep( 0.001 )
        # send the request for next data bytes
        self.i2c.writeto( self.addr, bytes([0xFB, 0x00]) )

        self.update()
        self.__angles = [0]*3 # Init angles
        self.__zeroJoyX = DEFAULT_ZERO_JOY_X # values for the joystick's zero pos
        self.__zeroJoyY = DEFAULT_ZERO_JOY_Y

    def update( self ):
        data = self.i2c.readfrom( self.addr, 6 ) # read 6 bytes
        if len(data)>5:
        	# Previous state
            self.__lastZ = self._buttonZ
            self.__lastC = self._buttonC
            self.__lastJoyX = self.joy_x
            self.__lastJoyY = self.joy_y

            # averageCounter ++;
            # if (averageCounter >= AVERAGE_N)
            #    averageCounter = 0;

            self._joyX = data[0]
            self._joyY = data[1]
            for i in range(3):
                # accelArray[i][averageCounter] = ((int)data[i+2] << 2) + ((data[5] & (B00000011 << ((i+1)*2) ) >> ((i+1)*2))); 
                self.__angles[i] = (data[i+2] << 2) + ((data[5] & (0b00000011 << ((i+1)*2) ) >> ((i+1)*2)))

                # accelYArray[averageCounter] = ((int)data[3] << 2) + ((data[5] & B00110000) >> 4); 
                # accelZArray[averageCounter] = ((int)data[4] << 2) + ((data[5] & B11000000) >> 6); 

            self._buttonZ = ( data[5] & 0b00000001) == 0
            self._buttonC = ((data[5] & 0b00000010) >> 1) == 0

            # increment button counter
            if self._buttonZ and not(self.__lastZ):
                self._countZ += 1
            if self._buttonC and not(self.__lastC):
                self._countC += 1 

            # send the request for next bytes
            self.i2c.writeto( self.addr, bytes([0x00]) )
    @property
    def c(self):
        """ Current state of button C """
        return self._buttonC

    @property
    def z(self):
        """ Current state of button Z """
        return self._buttonZ

    @property
    def c_count(self):
        """ count number of activation of C button since last property reading """
        r = self._countC
        self._countC = 0
        return r

    @property
    def z_count(self):
        """ count number of activation of Z button since last property reading """
        r = self._countZ
        self._countZ = 0
        return r
    
    @property 
    def joy_x( self ):
        """ Read joystick X position from -128 @ left to +128 @ right """
        return 0 if (self.__zeroJoyX-self.__joy_min_thres) < self._joyX < (self.__zeroJoyX+self.__joy_min_thres) else self._joyX - self.__zeroJoyX

    @property 
    def joy_y( self ):
        """ Read joystick X position from -128 @ rear to +128 @ front """
        return 0 if (self.__zeroJoyY-self.__joy_min_thres) < self._joyY < (self.__zeroJoyY+self.__joy_min_thres) else self._joyY - self.__zeroJoyY

    @property
    def joy_right( self ):
        """ Check if the joystick is now pushed to the right """
        return (self.joy_x > self.__joy_thres)

    @property
    def joy_left( self ):
        """ Check if the joystick is now pushed to the left """
        return (self.joy_x < (-1*self.__joy_thres))

    @property
    def joy_up( self ):
        """ Check if the joystick is now pushed to the front """
        return (self.joy_y > self.__joy_thres)

    @property
    def joy_down( self ):
        """ Check if the joystick is now pushed to the rear """
        return (self.joy_y < (-1*self.__joy_thres))

    @property
    def accel_x(self):
        """ read the value for accelerometer X """
        return float(self.__angles[0]) - ZEROX

    @property
    def accel_y(self):
        """ read the value for accelerometer Y """
        return float(self.__angles[1]) - ZEROY

    @property
    def accel_z(self):
        """ read the value for accelerometer Z """
        return float(self.__angles[2]) - ZEROZ

    @property
    def roll(self):
        return int( atan2(self.accel_x,self.accel_z)/ 3.14159265 * 180.0 )
    
    @property
    def pitch(self):
        val = self.accel_y/RADIUS
        if not( -1 <= val <= 1 ):
            val = 1 if val >0 else -1
        return int( acos( val )/ 3.14159265 * 180.0)
    
