"""
lcpi2c.py - a LiquidCrystal_I2C portage to MicroPython.

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Products:
---> https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/882-lcd-backpack-i2c-3232100008823.html
---> https://shop.mchobby.be/fr/nouveaute/1807-afficheur-lcd-16x2-i2c-3232100018075-dfrobot.html
---> https://shop.mchobby.be/fr/afficheur-lcd-tft-oled/881-lcd-20x4-backpack-i2c-blanc-sur-bleu-3232100008816.html

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  08 april 2020 - Dominique - initial portage from Arduino to MicroPython
"""
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
from machine import Pin, I2C
from time import sleep_ms, sleep_us

# commands
LCD_CLEARDISPLAY = 0x01
LCD_RETURNHOME   = 0x02
LCD_ENTRYMODESET = 0x04
LCD_DISPLAYCONTROL= 0x08
LCD_CURSORSHIFT  = 0x10
LCD_FUNCTIONSET  = 0x20
LCD_SETCGRAMADDR = 0x40
LCD_SETDDRAMADDR = 0x80

# flags for display entry mode
LCD_ENTRYRIGHT = 0x00
LCD_ENTRYLEFT  = 0x02
LCD_ENTRYSHIFTINCREMENT = 0x01
LCD_ENTRYSHIFTDECREMENT = 0x00

# flags for display on/off control
LCD_DISPLAYON  = 0x04
LCD_DISPLAYOFF = 0x00
LCD_CURSORON   = 0x02
LCD_CURSOROFF  = 0x00
LCD_BLINKON    = 0x01
LCD_BLINKOFF   = 0x00

# flags for display/cursor shift
LCD_DISPLAYMOVE = 0x08
LCD_CURSORMOVE  = 0x00
LCD_MOVERIGHT   = 0x04
LCD_MOVELEFT    = 0x00

# flags for function set
LCD_8BITMODE = 0x10
LCD_4BITMODE = 0x00
LCD_2LINE    = 0x08
LCD_1LINE    = 0x00
LCD_5x10DOTS = 0x04
LCD_5x8DOTS  = 0x00

# flags for backlight control
LCD_BACKLIGHT   = 0x08
LCD_NOBACKLIGHT = 0x00

LCD_EN = 0b00000100  # Enable bit
LCD_RW = 0b00000010  # Read/Write bit
LCD_RS = 0b00000001  # Register select bit


class LCDI2C():
	"""Base class to control LCD display via I2C bus."""

	def __init__(self, i2c, address=0x27, cols=2, rows=16, dotsize=LCD_5x8DOTS ):
		"""Initialize I2C LCD at specified I2C address on the I2C Bus."""
		self.address = address
		self.i2c = i2c
		self.cols = cols
		self.rows = rows
		self._backlightval = LCD_NOBACKLIGHT
		self._displayfunction = None
		self._displaycontrol  = None
		self._displaymode     = None

		# ========= Initialize screen ==========
		# When the display powers up, it is configured as follows:
		#
		# 1. Display clear
		# 2. Function set:
		#    DL = 1; 8-bit interface data
		#    N = 0; 1-line display
		#    F = 0; 5x8 dot character font
		# 3. Display on/off control:
		#    D = 0; Display off
		#    C = 0; Cursor off
		#    B = 0; Blinking off
		# 4. Entry mode set:
		#    I/D = 1; Increment by 1
		#    S = 0; No shift
		#
		# Note, however, that resetting the Arduino doesn't reset the LCD, so we
		# can't assume that its in that state when a sketch starts (and the
		# LiquidCrystal constructor is called).
		self._displayfunction = LCD_4BITMODE | LCD_1LINE | LCD_5x8DOTS
		if rows > 1:
			self._displayfunction = self._displayfunction | LCD_2LINE

		# for some 1 line displays you can select a 10 pixel high font
		if (dotsize != 0) and (lines == 1):
			self._displayfunction = self._displayfunction | LCD_5x10DOTS

		# SEE PAGE 45/46 FOR INITIALIZATION SPECIFICATION!
		# according to datasheet, we need at least 40ms after power rises above 2.7V before sending commands.
		sleep_ms(50)

 		# Now we pull both RS and R/W low to begin commands
		self.expanderWrite(self._backlightval) # reset expanderand turn backlight off (Bit 8 =1)
		sleep_ms( 1000 )

		# put the LCD into 4 bit mode this is according to the hitachi HD44780 datasheet
		# figure 24, pg 46

		# we start in 8bit mode, try to set 4 bit mode
		self.write4bits( 0x03 << 4 )
		sleep_us(4500) # wait min 4.1ms

		# second try
		self.write4bits( 0x03 << 4 )
		sleep_us(4500) # wait min 4.1ms

		# third go!
		self.write4bits( 0x03 << 4 )
		sleep_us(150)

		# finally, set to 4-bit interface
		self.write4bits( 0x02 << 4 )


		# set #lines, font size, etc.
		self.command( LCD_FUNCTIONSET | self._displayfunction ) # DisplayFunction

		# turn the display on with no cursor or blinking default
		self._displaycontrol = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
		self.display() # turn display on/off (quickly)

		#clear it off
		self.clear()

		# Initialize to default text direction (for roman languages)
		self._displaymode = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT

		# set the entry mode
		self.command( LCD_ENTRYMODESET | self._displaymode )

		self.home()


	def send( self, value, mode=LCD_RS ): # RegisterSelect bit by default
		""" write either command or data """
		highnib = value & 0xF0
		lownib=(value<<4) & 0xF0
		self.write4bits( highnib | mode )
		self.write4bits( lownib  | mode )

	def command( self, value ): # uint8_t
		""" Just send a command to LCD """
		self.send(value, mode=0)

	def write( self, value ): # uint_8
		""" Just send a data (a single byte) or bytearray to LCD """
		if (type(value) is bytearray) or (type(value) is bytes):
			for data in value:
				self.send( data, LCD_RS )
		else:
			self.send(value, LCD_RS )

	def write4bits( self, value ): # uint8_t
		""" Write a 4 bits values then pulse the Enable flag """
		self.expanderWrite( value )
		self.pulseEnable( value )

	def expanderWrite( self, _data ): # uint8_t
		""" Send data over I2C bus by including the BackLight flag """
		#Wire.beginTransmission(_Addr);
		#printIIC((int)(_data) | _backlightval) # print II
		self.i2c.writeto( self.address, bytes( [_data | self._backlightval] ))
		#Wire.endTransmission();

	def pulseEnable( self, _data ): # uint8_t
		""" Pulse the Enable Pin on the LCD """
		self.expanderWrite( _data | LCD_EN ) # En high
		sleep_us(1) # enable pulse must be >450ns

		self.expanderWrite( _data & (0xFF ^ LCD_EN) ) # En low
		sleep_us(50)  # commands need > 37us to settle


	# ============ high level commands, for the user! ============
	def clear( self ):
		self.command( LCD_CLEARDISPLAY ) # clear display, set cursor position to zero
		sleep_us( 2000 ) # this command takes a long time!

	def home( self ):
		""" Set the cursor @ home position """
		self.command( LCD_RETURNHOME ) # set cursor position to zero
		sleep_us( 2000 ) # this command takes a long time!

	def backlight( self, value=True ):
		""" Activate the backlight """
		if value:
			self._backlightval = LCD_BACKLIGHT
		else:
			self._backlightval = LCD_NOBACKLIGHT
		self.expanderWrite(0)

	def display( self, value=True ):
		""" turn on/off the display (quickly). Do not changes the backlight."""
		if value:
			self._displaycontrol |= LCD_DISPLAYON
		else:
			self._displaycontrol &= (0xFF ^ LCD_DISPLAYON)
		self.command( LCD_DISPLAYCONTROL | self._displaycontrol )

	def autoscroll( self, value=True ):
		""" Activate / Deactivate autoscrolling.
			value=True : 'Right Justify' text from the cursor.
			value=False: 'Left Justify' text from the cursor. """
		if value:
			#  This will 'right justify' text from the cursor
			self._displaymode |= LCD_ENTRYSHIFTINCREMENT
		else:
			# This will 'left justify' text from the cursor
			self._displaymode &= (0xFF ^ LCD_ENTRYSHIFTINCREMENT)
		self.command( LCD_ENTRYMODESET | self._displaymode )

	def create_char( self, index, charmap ):
		""" Allows to fill the first 8 CGRAM locations with custom characters

			:param index: index of the char to define (0-7)
			:param charmap: a byte object with 8 bytes """
		assert 0 <= index <= 7
		assert (type(charmap) is list) and (len(charmap)==8)

		index &= 0x7  # only8 locations 0-7
		self.command( LCD_SETCGRAMADDR | (index << 3) )
		for c in charmap:
			self.write(c)

	def cursor( self, value=True ):
		""" Display / Hide the cursor """
		if value:
			self._displaycontrol |= LCD_CURSORON
		else:
			self._displaycontrol &= (0xFF^LCD_CURSORON)
		self.command( LCD_DISPLAYCONTROL | self._displaycontrol )

	def blink( self, value=True ):
		""" blinking cursor """
		if value:
			self._displaycontrol |= LCD_BLINKON
		else:
			self._displaycontrol &= (0xFF^LCD_BLINKON)
		self.command( LCD_DISPLAYCONTROL | self._displaycontrol )

	def scroll_display( self, direction=LCD_MOVELEFT ):
		""" Scroll the display without changing the RAM """
		assert direction in (LCD_MOVELEFT,LCD_MOVERIGHT), "Invalid direction %s value" % direction
		self.command(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | direction)

	def right_to_left( self, value=True ):
		""" For text flowing from right to left (otherwise, it will flow from left to right) """
		if value:
			self._displaymode &= (0xFF ^ LCD_ENTRYLEFT)
		else:
			self._displaymode |= LCD_ENTRYLEFT
		self.command(LCD_ENTRYMODESET | self._displaymode);

	def set_cursor( self, pos ):
		""" set the cursor position with a 0 based tuple of (col,row) equivalent to the position x,y positionning """
		assert type( pos ) is tuple, "pos must be a tuple (col,row)"
		row_offsets = [ 0x00, 0x40, 0x14, 0x54 ]
		row = pos[1]
		if ( row > self.rows ):
			row = self.rows-1  # we count rows starting w/0

		self.command(LCD_SETDDRAMADDR | (pos[0] + row_offsets[row])) # Col + row offset

	def print( self, str, pos=None ):
		""" Display a string at the current cursor location.
		    Cursor may be repositionned before printing is pos is feeded with a (col,row) tuple. """
		if pos:
			self.set_cursor( pos )
		self.write( str.encode("ASCII") )
