""" HOLTEK HT1632C library for MicroPython

  written for DFRobot DFR0487

* Author: Meurisse Dominique for MCHobby SPRL
"""

__version__ = "0.1.0"
__repo__ = "https://github.com/mchobbyMCHobby/esp8266-upy/ht1632c.git"

from micropython import const
from machine import Pin
from framebuf import FrameBuffer, MONO_VLSB

HT1632_READ  = const(0x06)
HT1632_WRITE = const(0x05)
HT1632_COMMAND = const(0x04)

HT1632_SYS_DIS = const(0x00)
HT1632_SYS_EN  = const(0x01)

HT1632_LED_OFF = const(0x02)
HT1632_LED_ON  = const(0x03)

HT1632_BLINK_OFF = const(0x08)
HT1632_BLINK_ON  = const(0x09)

HT1632_SLAVE_MODE  = const(0x10)
HT1632_MASTER_MODE = const(0x14)

HT1632_INT_RC  = const(0x18)
HT1632_EXT_CLK = const(0x1C)

HT1632_PWM_CONTROL = const(0xA0)

HT1632_COMMON_8NMOS  = const(0x20)
HT1632_COMMON_16NMOS = const(0x24)
HT1632_COMMON_8PMOS  = const(0x28)
HT1632_COMMON_16PMOS = const(0x2C)

# Reversing the bit order (as it was readed from back to front)
# Source - https://stackoverflow.com/a/62431000
# Posted by theb33k, Retrieved 2026-06-20, License - CC BY-SA 4.0
LUT = [0, 128, 64, 192, 32, 160, 96, 224, 16, 144, 80, 208, 48, 176, 112, 240,
       8, 136, 72, 200, 40, 168, 104, 232, 24, 152, 88, 216, 56, 184, 120,
       248, 4, 132, 68, 196, 36, 164, 100, 228, 20, 148, 84, 212, 52, 180,
       116, 244, 12, 140, 76, 204, 44, 172, 108, 236, 28, 156, 92, 220, 60,
       188, 124, 252, 2, 130, 66, 194, 34, 162, 98, 226, 18, 146, 82, 210, 50,
       178, 114, 242, 10, 138, 74, 202, 42, 170, 106, 234, 26, 154, 90, 218,
       58, 186, 122, 250, 6, 134, 70, 198, 38, 166, 102, 230, 22, 150, 86, 214,
       54, 182, 118, 246, 14, 142, 78, 206, 46, 174, 110, 238, 30, 158, 94,
       222, 62, 190, 126, 254, 1, 129, 65, 193, 33, 161, 97, 225, 17, 145, 81,
       209, 49, 177, 113, 241, 9, 137, 73, 201, 41, 169, 105, 233, 25, 153, 89,
       217, 57, 185, 121, 249, 5, 133, 69, 197, 37, 165, 101, 229, 21, 149, 85,
       213, 53, 181, 117, 245, 13, 141, 77, 205, 45, 173, 109, 237, 29, 157,
       93, 221, 61, 189, 125, 253, 3, 131, 67, 195, 35, 163, 99, 227, 19, 147,
       83, 211, 51, 179, 115, 243, 11, 139, 75, 203, 43, 171, 107, 235, 27,
       155, 91, 219, 59, 187, 123, 251, 7, 135, 71, 199, 39, 167, 103, 231, 23,
       151, 87, 215, 55, 183, 119, 247, 15, 143, 79, 207, 47, 175, 111, 239,
       31, 159, 95, 223, 63, 191, 127, 255]

class HT1632C( FrameBuffer ):
    """ The base class for all HT1632C monochrome LED backpack. Based on DFR0487 """

    def __init__(self, data_pin, wr_pin, cs_pin, auto_write=True, brightness=1.0, width=24, height=8):
        self.data_pin = data_pin
        self.wr_pin = wr_pin
        self.cs_pin = cs_pin
        self.width = width
        self.height = height
        self.data_pin.init( Pin.IN ) # High impedance
        self.wr_pin.init( Pin.OUT )
        self.cs_pin.init( Pin.OUT )
        self.data_pin.value( 0 )
        self.wr_pin.value( 1 )
        self.cs_pin.value( 1 )

        self._buffer = bytearray(width*height//8) # 24*8 / 8
        super().__init__( self._buffer, width, height, MONO_VLSB )
           
        self.write_cmd( HT1632_SYS_EN ) # enable
        self.write_cmd( HT1632_LED_ON ) # power_leds
        self.write_cmd( HT1632_BLINK_OFF ) 
        self.write_cmd( HT1632_MASTER_MODE )
        self.write_cmd( HT1632_INT_RC )
        self.write_cmd( HT1632_COMMON_16NMOS )
        self.write_cmd( HT1632_PWM_CONTROL | 0xF ) 
     
        self._blink_rate = None
        self._brightness = None
        self.blink_rate = 0
        self.brightness = brightness
        self._auto_write = auto_write
        self._power_leds = True
        self._enable     = True 
        self.fill(0)
        self.show()

    def write_bits( self, data16, bitlen ):
        self.data_pin.init( Pin.OUT )
        self.data_pin.value( 1 )
        for i in range(bitlen,0,-1): # 16..1
            self.wr_pin.value(0)
            bit = (data16 & (1<<(i-1))) > 0
            #print('  ', int(bit) )
            self.data_pin.value( bit )
            self.wr_pin.value(1)
        self.data_pin.init( Pin.IN )		


    def write_cmd(self, cmd ):
        _v = (HT1632_COMMAND << 8) | cmd
        self.cs_pin.value( 0 )
        self.write_bits( _v<<1, 12 ) # write 12 bits
        self.cs_pin.value( 1 )

    @property
    def blink_rate(self):
        """The blink rate. Range 0-3."""
        return self._blink_rate

    @blink_rate.setter
    def blink_rate(self, rate=None):
        if not 0 <= rate <= 3:
            raise ValueError("Blink rate must be an integer in the range: 0-3")
        rate = rate & 0x03
        self._blink_rate = rate
        #self._write_cmd(_HT16K33_BLINK_CMD | _HT16K33_BLINK_DISPLAYON | rate << 1)
        if self._blink_rate > 0:
            self.write_cmd( HT1632_BLINK_ON )
        else:
            self.write_cmd( HT1632_BLINK_OFF )

    @property
    def brightness(self):
        """The brightness. Range 0.0-1.0"""
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        if not 0.0 <= brightness <= 1.0:
            raise ValueError("Brightness must be in range 0.0-1.0" )
        self._brightness = brightness
        _bright = round(15 * brightness)
        _bright = _bright & 0x0F
        self.write_cmd( HT1632_PWM_CONTROL | _bright )

    @property
    def power_leds( self ):
        """ Enable/disable LED powering """
        return self._power_leds

    @power_leds.setter
    def power_leds( self, value ):
        """ Enable/disable LED powering """
        self.write_cmd( HT1632_LED_ON if value else HT1632_LED_OFF )
        self._power_leds = value

    @property
    def enable( self ):
        """ Enable/disable power & oscillator for Power Saving"""
        return self._enable

    @enable.setter
    def enable( self, value ):
        self.write_cmd( HT1632_SYS_EN if value else HT1632_SYS_DIS )
        self._enable = value

    def show(self):
        """Refresh the display and show the changes."""        
        self.cs_pin.value(0)
        self.write_bits( HT1632_WRITE, 3 )	
        self.write_bits( 0, 7 )
        for i in range(24):
        	# Reversing the bits order with LUT. LUT[ 0b11010010 ] = 0b01001011
            self.write_bits( LUT[self._buffer[i]]<<8, 16 ) 
        self.cs_pin.value(1)
