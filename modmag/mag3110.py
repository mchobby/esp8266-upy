"""
mag3110 is a micropython module for the Sparkfun MAG3110 or Olimex MOD-MAG board. 

MAG3110 is a Freescale Semiconductor 3 axis digital magnetometer

MOD-MAG board : http://shop.mchobby.be/product.php?id_product=1413
MOD-MAG : https://www.olimex.com/Products/Modules/Sensors/MOD-MAG/open-source-hardware  
User Guide : https://www.olimex.com/Products/Modules/Sensors/MOD-MAG/resources/MOD-MAG.pdf 

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
from time import sleep_us, sleep, time
from math import atan2

# MAG3110 Magnetometer Registers 
DR_STATUS	= 0x00
OUT_X_MSB	= 0x01
OUT_X_LSB	= 0x02
OUT_Y_MSB	= 0x03
OUT_Y_LSB	= 0x04
OUT_Z_MSB	= 0x05
OUT_Z_LSB	= 0x06
WHO_AM_I	= 0x07
SYSMOD		= 0x08
OFF_X_MSB	= 0x09
OFF_X_LSB	= 0x0A
OFF_Y_MSB	= 0x0B
OFF_Y_LSB	= 0x0C
OFF_Z_MSB	= 0x0D
OFF_Z_LSB	= 0x0E
DIE_TEMP	= 0x0F
CTRL_REG1	= 0x10
CTRL_REG2	= 0x11

WHO_AM_I_RESP = 0xC4

# CTRL_REG1 Settings
#    Output Data Rate/Oversample Settings
#    DR_OS_80_16 -> Output Data Rate = 80Hz, Oversampling Ratio = 16

DR_OS_80_16 	= 0x00
DR_OS_40_32 	= 0x08
DR_OS_20_64 	= 0x10
DR_OS_10_128	= 0x18
DR_OS_40_16		= 0x20
DR_OS_20_32		= 0x28
DR_OS_10_64		= 0x30
DR_OS_5_128		= 0x38
DR_OS_20_16		= 0x40
DR_OS_10_32		= 0x48
DR_OS_5_64		= 0x50
DR_OS_2_5_128	= 0x58
DR_OS_10_16		= 0x60
DR_OS_5_32		= 0x68
DR_OS_2_5_64	= 0x70
DR_OS_1_25_128	= 0x78
DR_OS_5_16		= 0x80
DR_OS_2_5_32	= 0x88
DR_OS_1_25_64	= 0x90
DR_OS_0_63_128	= 0x98
DR_OS_2_5_16	= 0xA0
DR_OS_1_25_32	= 0xA8
DR_OS_0_63_64	= 0xB0
DR_OS_0_31_128	= 0xB8
DR_OS_1_25_16	= 0xC0
DR_OS_0_63_32	= 0xC8
DR_OS_0_31_64	= 0xD0
DR_OS_0_16_128	= 0xD8
DR_OS_0_63_16	= 0xE0
DR_OS_0_31_32	= 0xE8
DR_OS_0_16_64	= 0xF0
DR_OS_0_08_128	= 0xF8

# Other CTRL_REG1 Settings
FAST_READ 			= 0x04
TRIGGER_MEASUREMENT	= 0x02
ACTIVE_MODE			= 0x01
STANDBY_MODE		= 0x00

# CTRL_REG2 Settings
AUTO_MRST_EN		= 0x80
RAW_MODE			= 0x20
NORMAL_MODE			= 0x00
MAG_RST				= 0x10

# SYSMOD Readings
SYSMOD_STANDBY		= 0x00
SYSMOD_ACTIVE_RAW	= 0x01
SYSMOD_ACTIVE		= 0x02

OFFSET_X_AXIS = 0x09 #1
OFFSET_Y_AXIS = 0x0B #3
OFFSET_Z_AXIS = 0x0D #5

CALIBRATION_TIMEOUT = 5 # seconds 
DEG_PER_RAD = (180.0/3.14159265358979)

class MAG3110():
    """
    Class to control the mag3110 board.

    Based on the SparkFun library for mag3110
    """


    def __init__( self, i2c_bus, addr=0x0E ):
        self.i2c    = i2c_bus # Initialized I2C bus 
        self.addr   = addr # MOD-LCD1x9 board address

        # Just some random initial values (updated by calibration)
        self.x_offset = 0
        self.y_offset = 0

        self.x_scale = 0.0
        self.y_scale = 0.0

        # used by reset 
        self.calibrationMode = False
        self.activeMode = False
        self.rawMode = False
        self.calibrated = False


        if self.who_am_i() != WHO_AM_I_RESP:
            raise Exception( 'MAG3110 not found!' ) 

        self.reset()
    
    def who_am_i( self ):
    	data = self.i2c.readfrom_mem( self.addr, WHO_AM_I, 1 )
        return data[0] # transform b'\xc4' --> value

    def enter_standby( self ):
    	""" MAG must be in standby mode when manipulating the REGx """
        self.activeMode = False
        data = self.i2c.readfrom_mem( self.addr, CTRL_REG1, 1 )
        current = data[0]
        # Clear bits 0 and 1 to enter low power standby mode
        self.i2c.writeto_mem( self.addr, CTRL_REG1, bytes([ current & (0xFF - 0x03) ]) )

    def exit_standby( self ):
        self.activeMode = True
        data = self.i2c.readfrom_mem( self.addr, CTRL_REG1, 1 )
        current = data[0]
        self.i2c.writeto_mem( self.addr, CTRL_REG1, bytes([ current | ACTIVE_MODE ]) ) 

    def enter_calibration( self ):
        """ Sets the output data rate @ highest and activate the mag sensor.
            Calibration on X et Y axis only. """
        self.calibrationMode = True
        self.calibrated = False
        # Starting values for calibration
        self.x_min = 32767
        self.x_max = -32768
        self.y_min = 32767
        self.y_max = -32768
        self.timeLastChange = None

        # activate raw readings for calibration
        self.set_rawdata_mode( True )

        # Highest DR_OS continous readings (data_rate = 80Hz, oversampling data = 16)
        self.setDR_OS( DR_OS_80_16 );

        # Activate
        if not(self.activeMode):
            self.start()

    def exit_calibration( self ):
        """ exit calibration mode """
        # Calculate offsets
        self.x_offset = (self.x_min + self.x_max)//2
        self.y_offset = (self.y_min + self.y_max)//2

        self.x_scale = 1.0/(self.x_max - self.x_min)
        self.y_scale = 1.0/(self.y_max - self.y_min)

        # Set the offset on MAG
        self.set_offset( OFFSET_X_AXIS, self.x_offset )
        self.set_offset( OFFSET_Y_AXIS, self.y_offset )

        # Use the offsets when reading (normal mode)
        self.set_rawdata_mode( False )

        self.calibrationMode = False
        self.calibrated = True

        # Enter standby and wait
        # self.enter_standby()

    def step_calibration( self ):
        """ Must call every time to collect calibration data.
            Calibration will automatically exit when enough data is collected (about 5 to 10 sec).
            You can terminate calibration sooner with exit_calibration() """
        xyz = self.read()

        # detect if min/max has changed
        changed = False
        if xyz[0] < self.x_min:
        	self.x_min = xyz[0]
        	changed = True
        if xyz[0] > self.x_max:
            self.x_max = xyz[0]
            changed = True

        if xyz[1] < self.y_min: 
            self.y_min = xyz[1]
            changed = True
        if xyz[1] > self.y_max:
            self.y_max = xyz[1]
            changed = True

        if changed:
            self.timeLastChange = time() # Reset timeout counter

        # If the timeout has been reached, exit calibration
        if self.timeLastChange and ( (time()-self.timeLastChange) > CALIBRATION_TIMEOUT ):
        	self.exit_calibration()


    def set_offset( self, axis_register, offset ):
        """ Set an INT offset for a given axis """
        offset = offset << 1

        buff = ustruct.pack('>h', offset) # signed int on 2 bytes --> MSB first, 2's complement
        self.i2c.writeto_mem( self.addr, axis_register, bytes([ buff[0] ]) )
        sleep( 0.015 )
        self.i2c.writeto_mem( self.addr, axis_register+1, bytes([ buff[1] ]) )    	

    def reset( self ):
        """ reset the library and configure the MAG """
        # REG1 Bit mask: DR2 | DR1 | DR0 | OS1 | OS0 | FR | TM | AC 
        # DR2=0, DR1=0, DR0=0 , OS1=0, OS2=0 --> 
        # FR=0 --> Full 16 bit values read
        # TM=0 --> Normal condition 
        # AC=0 --> Standby mode (between measurement)
        self.i2c.writeto_mem( self.addr, CTRL_REG1, bytes([0x00]) ) # Set everything to 0

        # REG2 Bit mask: AUTO_MRST_EN | - | RAW | Mag_RST | - | - | - | - 
        # AUTO_MRST_EN = 1 --> Automatic reset of magnetic sensor before data acquisition
        # RAW     = 0 --> Normal mode, data value are corrected by user offset register values
        # Mag_RST = 0 --> Reset cycle not activated (one-shot)        
        self.i2c.writeto_mem( self.addr, CTRL_REG2, bytes([0x80]) ) # Enable Auto Mag Reset, non-raw mode
        
        self.calibrationMode = False
        self.activeMode = False
        self.rawMode = False
        self.calibrated = False
	
        self.set_offset( OFFSET_X_AXIS, 0)
        self.set_offset( OFFSET_Y_AXIS, 0)
        self.set_offset( OFFSET_Z_AXIS, 0)

    def setDR_OS( self, DROS ):
        """ Set the DR_OS configuration which fix data_rate (hz) and over_sampling """
        wasActive = self.activeMode

        if self.activeMode:
            self.enter_standby() # Must be in standby to modify CTRL_REG1

        # If we attempt to write to CTRL_REG1 right after going into standby
        # It might fail to modify the other bits
        sleep( 0.100 )

        # Get the current control register
        data = self.i2c.readfrom_mem( self.addr, CTRL_REG1, 1 )
        current = data[0] & 0x07 # And chop off the 5 MSB (remove the current DR_OS configuration)
        self.i2c.writeto_mem( self.addr, CTRL_REG1, bytes([ current | DROS ]) )# Write back the register with new DR_OS set

        sleep( 0.100 )

        # Start sampling again if we were before
        if wasActive:
            self.exit_standby()

    def set_rawdata_mode( self, activated ):
    	""" Activate raw mode = non-user corrected """  
    	
    	# Note that AUTO_MRST_EN will always read back as 0
        # Therefore we must explicitly set this bit every time we modify CTRL_REG2
        if activated: # non-user corrected
            self.rawMode = True
            self.i2c.writeto_mem( self.addr, CTRL_REG2, bytes([ AUTO_MRST_EN | (0x01 << 5)  ]) )
        else:  # Turn off raw mode
            self.rawMode = False
            self.i2c.writeto_mem( self.addr, CTRL_REG2, bytes([ AUTO_MRST_EN & (0xFF-(0x01 << 5)) ]) )        

    def start( self ):
        self.exit_standby()

    @property
    def is_active( self ):
        return self.activeMode

    def is_raw( self ):
        return self.rawMode

    @property
    def is_calibrated( self ):
        return self.calibrated

    @property
    def is_calibrating( self ):
        return self.calibrationMode

    def user_offset( self ):
        """ Read the user offset stored in the component """

        data = [0x00] * 2

        data = self.i2c.readfrom_mem( self.addr, 0x09, 2) # read 2 bytes
        x = ustruct.unpack( '>h', data[0:2] )[0] # convert 2 bytes, MSB first to integer, int 2's complement 

        data = self.i2c.readfrom_mem( self.addr, 0x0B, 2) # read 2 bytes
        y = ustruct.unpack( '>h', data[0:2] )[0]

        data = self.i2c.readfrom_mem( self.addr, 0x0D, 2) # read 2 bytes
        z = ustruct.unpack( '>h', data[0:2] )[0]
        #WaitMicrosecond(2000);
        return (x>>1,y>>1,z>>1)	

    @property
    def data_ready( self ):
        """ DR bitmask (ZYXOW, ZOW, YOW, XOW, ZYXDR, ZDR, YDR, XDR)
            xOW is overwrite flag, previous xyz value where overwrite before reading
            xDR is new data ready for axis """
        data = self.i2c.readfrom_mem( self.addr, DR_STATUS, 1 )
        # Check if ZYXDR bit is active
        return data[0] & 8==8

    def read( self ):
        """ read x,y,z values from MAG. Return the values as a tuple """ 
 
        # Start readout at X MSB address
        data = self.i2c.readfrom_mem( self.addr, OUT_X_MSB, 6 )

        x = ustruct.unpack( '>h', data[0:2] )[0] # convert 2 bytes, MSB first to integer, signed 2's complement number
        y = ustruct.unpack( '>h', data[2:4] )[0] 
        z = ustruct.unpack( '>h', data[4:6] )[0]        
        return x,y,z

    def heading( self ):
    	""" Return north indication in degree. """
        assert self.calibrated, "Not calibrated!"

        x,y,z = self.read()

        # Calculate the heading
        return atan2( -1*y*self.y_scale, x*self.x_scale) * DEG_PER_RAD
