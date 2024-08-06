"""
serlcd.py - a SparkFun SerLCD (LCD-16397) portage to MicroPython.

based on former work https://github.com/sparkfun/Qwiic_SerLCD_Py/blob/main/qwiic_serlcd.py

* Author(s): Meurisse D. from MCHobby (shop.mchobby.be).

Products:
	[SparkFun 16x2 SerLCD - RGB Backlight (Qwiic)](https://www.sparkfun.com/products/16396)
	[SparkFun 16x2 SerLCD - RGB Text (Qwiic)](https://www.sparkfun.com/products/16397)
	[SparkFun 20x4 SerLCD - RGB Backlight (Qwiic)](https://www.sparkfun.com/products/16398)

MCHobby investit du temps et des ressources pour écrire de la
documentation, du code et des exemples.
Aidez nous à en produire plus en achetant vos produits chez MCHobby.

------------------------------------------------------------------------

History:
  05 august 2024 - Dominique - initial portage from Arduino to MicroPython
"""

from micropython import const
import time

__version__ = '0.1.0'

MAX_ROWS = const(4)
MAX_COLUMNS = const(20)

# OpenLCD command characters
SPECIAL_COMMAND = const(254)  # Magic number for sending a special command
SETTING_COMMAND = const(0x7C) # 124, |, the pipe character: The command to change settings: baud, lines, width, backlight, splash, etc

# OpenLCD commands
CLEAR_COMMAND = const(0x2D)					 # 45, -, the dash character: command to clear and home the display
CONTRAST_COMMAND = const(0x18)				 # Command to change the contrast setting
ADDRESS_COMMAND = const(0x19)				 # Command to change the i2c address
SET_RGB_COMMAND = const(0x2B)				 # 43, +, the plus character: command to set backlight RGB value
ENABLE_SYSTEM_MESSAGE_DISPLAY = const(0x2E)  # 46, ., command to enable system messages being displayed
DISABLE_SYSTEM_MESSAGE_DISPLAY = const(0x2F) # 47, /, command to disable system messages being displayed
ENABLE_SPLASH_DISPLAY = const(0x30)			 # 48, 0, command to enable splash screen at power on
DISABLE_SPLASH_DISPLAY = const(0x31)		 # 49, 1, command to disable splash screen at power on
SAVE_CURRENT_DISPLAY_AS_SPLASH = const(0x0A) # 10, Ctrl+j, command to save current text on display as splash

# special commands
LCD_RETURNHOME = const(0x02)
LCD_ENTRYMODESET = const(0x04)
LCD_DISPLAYCONTROL = const(0x08)
LCD_CURSORSHIFT = const(0x10)
LCD_SETDDRAMADDR = const(0x80)

# flags for display entry mode
LCD_ENTRYRIGHT = const(0x00)
LCD_ENTRYLEFT = const(0x02)
LCD_ENTRYSHIFTINCREMENT = const(0x01)
LCD_ENTRYSHIFTDECREMENT = const(0x00)

# flags for display on/off control
LCD_DISPLAYON = const(0x04)
LCD_DISPLAYOFF = const(0x00)
LCD_CURSORON = const(0x02)
LCD_CURSOROFF = const(0x00)
LCD_BLINKON = const(0x01)
LCD_BLINKOFF = const(0x00)

# flags for display/cursor shift
LCD_DISPLAYMOVE = const(0x08)
LCD_CURSORMOVE = const(0x00)
LCD_MOVERIGHT = const(0x04)
LCD_MOVELEFT = const(0x00)

def map(x, in_min, in_max, out_min, out_max):
    return int((x-in_min) * (out_max-out_min) / (in_max-in_min) + out_min)

class SerLCD():
	"""Base class to control SparkFun SerLCD (LCD-16397) over I2C bus."""

	def __init__(self, i2c, address=0x72, cols=2, rows=16 ):
		"""Initialize I2C LCD at specified I2C address on the I2C Bus."""
		self.address = address
		self.i2c = i2c
		self.cols = cols
		self.rows = rows

		# self._backlightval = LCD_NOBACKLIGHT
		# self._displayfunction = None
		self._displaycontrol  = LCD_DISPLAYON | LCD_CURSOROFF | LCD_BLINKOFF
		self._displaymode     = LCD_ENTRYLEFT | LCD_ENTRYSHIFTDECREMENT
		self._backlight       = (255,255,255)
		self.buf4 = bytearray(4)
		self.buf1 = bytearray(1)
		self.buf10 = bytearray(10)

		# set default settings, as defined in constructor
		self.special_cmd(LCD_DISPLAYCONTROL | self._displaycontrol)
		time.sleep_ms(100)
		self.special_cmd(LCD_ENTRYMODESET | self._displaymode)
		time.sleep_ms(100)
		self.clear()
		time.sleep_ms(100)


	def special_cmd(self, command, count = 1):
		""" Send one (or multiple) special commands to the display.
			:param command: Command to send (a single byte)
			:param count: Number of times to send the command (if ommited, then default is once) """
		for i in range(0, count): # send the complete bytes (special command + command)
			self.i2c.writeto_mem( self.address, SPECIAL_COMMAND, bytes([command]) )
		time.sleep_ms(50)

	def cmd(self, command):
		""" Send one setting command to the display.
			:param command: Command to send (a single byte) """
		self.i2c.writeto_mem( self.address, SETTING_COMMAND, bytes([command]) )
		time.sleep_ms(10)


	# Keeps same methods as lcdi2c driver
	def clear(self):
		""" Sends the command to clear the screen. Returns True if successful """
		self.cmd(CLEAR_COMMAND)
		time.sleep_ms(10)

	def home(self):
		""" Set the cursor @ home position """
		pass

	def backlight( self, rgb ):
		""" User function to set the RGB backlight. This method calculates a
		    compensated valued (for better rendering) then apply it to LCD.
			The compensated value is saved for display on/off features.

		    rgb parameter is a tuple with each of r,g,b value from (0-255)"""

		if rgb==None: # Restore last saved value?
			rgb = self._backlight
		else:
			self._backlight = rgb

		# map our incoming values (0-255) to the backlight command range (0-29)
		red = 128 + map(rgb[0], 0, 255, 0, 29)
		green = 158 + map(rgb[1], 0, 255, 0, 29)
		blue = 188 + map(rgb[2], 0, 255, 0, 29)

		# Turn display off to hide confirmation messages
		self._displaycontrol &= (0xFF^LCD_DISPLAYON)
		self.buf10[0] = SPECIAL_COMMAND
		self.buf10[1] = (LCD_DISPLAYCONTROL | self._displaycontrol)

		#Set the red, green and blue values
		self.buf10[2] = SETTING_COMMAND
		self.buf10[3] = red
		self.buf10[4] = SETTING_COMMAND
		self.buf10[5] = green
		self.buf10[6] = SETTING_COMMAND
		self.buf10[7] = blue

		# Turn display back on and end
		self._displaycontrol |= LCD_DISPLAYON
		self.buf10[8] = SPECIAL_COMMAND
		self.buf10[9] = (LCD_DISPLAYCONTROL | self._displaycontrol)

		# send the complete bytes (address, settings command , contrast command, contrast value)
		self.i2c.writeto_mem(self.address, SETTING_COMMAND, self.buf10 )
		time.sleep_ms(50)


	def _fast_backlight( self, rgb=None ):
		""" Quickly set the backlight value"""
		self.buf4[0] = SET_RGB_COMMAND # command
		self.buf4[1] = rgb[0]
		self.buf4[2] = rgb[1]
		self.buf4[3] = rgb[2]
		self.i2c.writeto_mem( self.address, SETTING_COMMAND, self.buf4 )
		time.sleep_ms(10)


	def display( self, value=True ):
		""" turn on/off the display (quickly). Do not changes the backlight."""
		if value:
			self._fast_backlight( self._backlight )
			self._displaycontrol |= LCD_DISPLAYON
		else:
			self._fast_backlight( (0,0,0) )
			self._displaycontrol &= (0xFF^LCD_DISPLAYON)
		self.special_cmd(LCD_DISPLAYCONTROL | self._displaycontrol)


	def contrast( self, value ):
		""" Set the contrast from 0-250 (low is better for LCD-16397)"""
		self.i2c.writeto( self.address, bytes([SETTING_COMMAND, CONTRAST_COMMAND,value]))
		time.sleep_ms(10)

	def autoscroll( self, value=True ):
		""" Activate / Deactivate autoscrolling.
			value=True : 'Right Justify' text from the cursor.
			value=False: 'Left Justify' text from the cursor. """
		if value:
			self._displaycontrol |= LCD_ENTRYSHIFTINCREMENT
		else:
			self._displaycontrol &= (0xFF^LCD_ENTRYSHIFTINCREMENT)
		self.special_cmd(LCD_ENTRYMODESET | self._displaycontrol)


	def create_char( self, index, charmap ):
		""" Allows to fill the first 8 CGRAM locations with custom characters

			:param index: index of the char to define (0-7)
			:param charmap: a byte object with 8 bytes """
		assert 0 <= index <= 7
		assert (type(charmap) is list) and (len(charmap)==8)
		pass


	def cursor( self, value=True ):
		""" Display / Hide the underline cursor """
		if value:
			self._displaycontrol |= LCD_CURSORON
		else:
			self._displaycontrol &= (0xFF^LCD_CURSORON)
		self.special_cmd( LCD_DISPLAYCONTROL | self._displaycontrol )


	def move_cursor( self, left=True, count=1 ):
		if left:
			self.special_cmd( LCD_CURSORSHIFT | LCD_CURSORMOVE | LCD_MOVELEFT, count )
		else:
			self.special_cmd(LCD_CURSORSHIFT | LCD_CURSORMOVE | LCD_MOVERIGHT, count)

	def set_cursor(self, pos ):
		""" Set the cursor position to a particular (column,row).
			The column postion (0-19). The row postion (0-3) """
		row_offsets = [0x00, 0x40, 0x14, 0x54]
		# keep variables in bounds
		row = max(0, pos[1])            # row cannot be less than 0
		row = min(row, (MAX_ROWS - 1)) # row cannot be greater than max rows
		# construct the cursor "command"
		value = LCD_SETDDRAMADDR + (pos[0] + row_offsets[row])
		# send the complete bytes (special command + command)
		self.i2c.writeto( self.address, bytes([SPECIAL_COMMAND, value]) )


	def home( self ):
		self.special_cmd( LCD_RETURNHOME )
		time.sleep_ms(10)


	def blink( self, value=True ):
		""" blinking cursor """
		if value:
			self._displaycontrol |= LCD_BLINKON
		else:
			self._displaycontrol &= (0xFF^LCD_BLINKON)
		self.special_cmd( LCD_DISPLAYCONTROL | self._displaycontrol)

	def scroll_display( self, direction=LCD_MOVELEFT ):
		""" Scroll the display without changing the RAM """
		self.special_cmd(LCD_CURSORSHIFT | LCD_DISPLAYMOVE | direction, count)

	def right_to_left( self, value=True ):
		""" For text flowing from right to left (otherwise, it will flow from left to right) """
		if value:
			self._displaycontrol &= (0xFF^LCD_ENTRYLEFT)
		else:
			self._displaycontrol |= LCD_ENTRYLEFT
		self.special_cmd( LCD_ENTRYMODESET | self._displaycontrol )

	def system_messages( self, enable ):
		""" Enable/disable messages like 'Contrast: 5' """
		self.cmd( ENABLE_SYSTEM_MESSAGE_DISPLAY if enable else DISABLE_SYSTEM_MESSAGE_DISPLAY )
		time.sleep_ms(10)

	def splash( self, enable ):
		""" Enable/disable splash at startup """
		self.cmd( ENABLE_SPLASH_DISPLAY if enable else DISABLE_SPLASH_DISPLAY )
		time.sleep_ms(10)

	def save_splash( self ):
		""" Save current display content as Splash screen """
		self.cmd( SAVE_CURRENT_DISPLAY_AS_SPLASH )
		time.sleep_ms( 10 )

	def set_address( self, new_i2c_addr ):
		""" Permanently change the SerLCD I2C address to new_i2c_addr """
		self.i2c.writeto(self.address, bytes([SETTING_COMMAND, ADDRESS_COMMAND, new_i2c_addr]) )
		time.sleep_ms(50)

	def create_char( self, id, charmap ):
		""" Create a custom char for id (0..7) """
		assert 0<=id<=7, "Invalid id"

		self.buf10[0] = 27+id
		for i in range(1,9):
			self.buf10[i] = charmap[i-1]
		self.i2c.writeto_mem( self.address, SETTING_COMMAND, self.buf10 )
		time.sleep_ms( 50 )

	def write_char( self, id ):
		""" Display a custom char on the screen """
		assert 0<=id<=7, "Invalid id"
		self.cmd(35 + id)
		time.sleep_ms( 50 )

	def print( self, str, pos=None ):
		""" Display a string at the current cursor location.
		    Cursor may be repositionned before printing is pos is feeded with a (col,row) tuple. """
		if pos:
			self.set_cursor( pos )
		self.i2c.writeto( self.address, str.encode("ASCII") )
		time.sleep_ms(10)
