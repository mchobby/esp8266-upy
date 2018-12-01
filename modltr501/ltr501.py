"""
 ltr501 is a micropython module for the MOD-LTR-501ALS Olimex board. 

LTR-501ALS is an optical sensor of Lite-ON technology.
It can measure visible light from 0.01 Lux to  64000 Lux with linear response.
The onboard LED controler can be used to use the board as proximty sensor (up to 10cm).


MOD-LTR-501ALS board : http://shop.mchobby.be/product.php?id_product=1415
MOD-LTR-501ALS board : https://www.olimex.com/Products/Modules/Sensors/MOD-LTR-501ALS/open-source-hardware  
Arduino code sample  : https://github.com/OLIMEX/UEXT-MODULES/tree/master/MOD-LTR-501ALS/ARDUINO%20EXAMPLE

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
"""
import ustruct
# from time import sleep_us, sleep, time

ALS_CONTR      = 0x80
PS_CONTR       = 0x81
PS_LED         = 0x82
PS_N_PULSES    = 0x83
PS_MEAS_RATE   = 0x84
ALS_MEAS_RATE  = 0x85
PART_ID        = 0x86
WHO_AM_I       = 0x86
MANUFAC_ID     = 0x87 # should returns 0x05
ALS_DATA_CH1_0 = 0x88
ALS_DATA_CH1_1 = 0x89
ALS_DATA_CH0_0 = 0x8A
ALS_DATA_CH0_1 = 0x8B
ALS_PS_STATUS  = 0x8C
PS_DATA_0      = 0x8D
PS_DATA_1      = 0x8E
INTERRUPT      = 0x8F
PS_THRES_UP_0  = 0x90
PS_THRES_UP_1  = 0x91
PS_THRES_LOW_0 = 0x92
PS_THRES_LOW_1 = 0x93
ALS_THRES_UP_0 = 0x97
ALS_THRES_UP_1_= 0x98
ALS_THRES_LOW_0= 0x99
ALS_THRES_LOW_1= 0x9A
INTERRUPT_PERSIST = 0x9E 

WHO_AM_I_RESP = 0x80

DR_LUX       = 0x04 # ALS Lux Sensor Data Data Ready
DR_PROXIMITY = 0x01 # PS  Proximity Sensor Data Ready

LUX_RANGE_64K = 0x00 # ALS Dynamic Gain 2 Lux to 64.000 Lux
LUX_RANGE_320 = 0x08 # ALS Dynamic Gain 0.01 Lux to 320 Lux

class LTR_501ALS():
    """
    Class to control the LTR-501ALS board.
    """


    def __init__( self, i2c_bus, addr=0x23, lux_range = LUX_RANGE_64K ):
        self.i2c    = i2c_bus # Initialized I2C bus 
        self.addr   = addr # LTR_501ALS board address

        if self.who_am_i() != WHO_AM_I_RESP:
            raise Exception( 'LTR_501ALS not found!' ) 
    
        self.init( lux_range )
    
    def who_am_i( self ):
        data = self.i2c.readfrom_mem( self.addr, WHO_AM_I, 1 )
        return data[0] # transform b'\xc4' --> value

    def init( self, lux_range ):
        self.i2c.writeto_mem( self.addr, ALS_CONTR    , bytes([0x03 | lux_range ]) ) # ALS (Lux Sensor) in Active mode, 64k lux range
        self.i2c.writeto_mem( self.addr, PS_CONTR     , bytes([0x03]) ) # PS (proximity sensor) active mode, x1 GAIN
        self.i2c.writeto_mem( self.addr, PS_LED       , bytes([0x6B]) ) # LED 60Hz, 50% duty, 50mA
        self.i2c.writeto_mem( self.addr, PS_N_PULSES  , bytes([0x7F]) ) # 127 pulses
        self.i2c.writeto_mem( self.addr, PS_MEAS_RATE , bytes([0x02]) ) # PS 100ms measure rate
        self.i2c.writeto_mem( self.addr, ALS_MEAS_RATE, bytes([0x03]) ) # ALS Integration 100ms, repeat rate 500ms

    @property
    def data_ready( self ):
        """ Check if some data are ready for Lux Sensor (ALS) or Poximity Sensor (PS).

            Will return a list including DR_LUX (0x04) and/or DR_PROXIMITY (0x01) """
        data = self.i2c.readfrom_mem( self.addr, ALS_PS_STATUS, 1 )
        _r = []
        if data[0] & DR_LUX:
            _r.append( DR_LUX )
        if data[0] & DR_PROXIMITY:
            _r.append( DR_PROXIMITY )
        return _r

    @property
    def lux( self ):
        """ Extract ALS Lux Sensor value. Returns a tuple (ALS_0, ALS_1) probably for (visible_light, ) """
        data = self.i2c.readfrom_mem( self.addr, ALS_DATA_CH1_0, 4 )
        ADC_1 = ustruct.unpack( '<H', data[0:2] )[0] # convert 2 bytes, LSB first to integer, Unsigned number
        ADC_0 = ustruct.unpack( '<H', data[2:4] )[0] 
        return ( ADC_0, ADC_1 ) 

    @property
    def proximity(self):
        """ Extract PS Proximity Sensor value. returns a tuple (sensor_value, cm) """
        data = self.i2c.readfrom_mem( self.addr, PS_DATA_0, 2 )
        value = ustruct.unpack( '<H', data[0:2] )[0] # convert 2 bytes, LSB first to integer, Unsigned number
        cm = 10.0 - (10/2047)*value
        return (value,cm)
    

    #@property
    #def is_active( self ):
    #    return self.activeMode

