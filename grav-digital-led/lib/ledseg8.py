"""
8-Digital LED segment display module (DFR0646)
==============================================

MicroPython VK16K33 library to support DFR0646 digital display from DFRobot.

DFR0646 - 8-Digital LED segment display module V1.0
  <https://www.dfrobot.com/product-1967.html> (Product ID: DFR0646)

inspired from VK16K33 Arduino library from FreeNove LED matrix @
	https://github.com/Freenove/Freenove_VK16K33_Lib/tree/main
Inspired from Dawid Stankiewicz (stonatm) for DFR0645 using TM1650 driver
	https://github.com/stonatm/tm1650_micropython

History
-------
Dec 12, 2023 - Meurisse D. - Initial writing, portage from Arduino code

"""
import time
from micropython import const

# different commands
VK16K33_DISP_DATA  = const(0x00) # R/W. Display data pointer (base addr)
VK16K33_KEY_DATA   = const(0x40) # R only. Key data pointer (base addr)
VK16K33_INT_DATA   = const(0x60) # R only. Interrupt Flag signal.
VK16K33_SYS_SETUP  = const(0x20) # [CMD] W only. Add required configuration bits
VK16K33_DISP_SETUP = const(0x80) # [CMD] W only. Add on/off bit and blink bits
VK16K33_ROW_SETUP  = const(0xA0) # [CMD] W only. Add bits to defines INT/ROW output pin.
VK16K33_DIM_SETUP  = const(0xE0) # [CMD] W only. Add bits to set Dimming level

# VK16K33_DISP_SETUP options
VK16K33_DISPLAY_OFF = const(0x00)
VK16K33_DISPLAY_ON  = const(0x01)
VK16K33_BLINK_OFF   = const(0x00)
VK16K33_BLINK_1HZ   = const(0x02)
VK16K33_BLINK_2HZ   = const(0x04)
VK16K33_BLINK_0HZ5  = const(0x06)

class LedSegment8():
  """ VK16K33 8-Digital LED Segment Display module (DFR0646) driver for MicroPython """

  def __init__(self, i2c, addr=0x70 ):
    self.dbuf = bytearray(16)
    self.tbuf = bytearray(1) # Temporary buffer
    self._display_status = VK16K33_DISPLAY_OFF
    self._blink_status   = VK16K33_BLINK_OFF
    self.i2c  = i2c
    self.addr = addr
    # System setup
    self.tbuf[0] = VK16K33_SYS_SETUP | 0x01
    self.i2c.writeto( self.addr, self.tbuf )
    # Display On & Blink Off
    self.blink_off()
    self.on()
    # brightness
    self.brightness( 15 )

  def int(self, num):
    """ Show integer (9999 9999 to -999 9999) """
    if (num >= 0) and (num <= 99999999):
      t = str(int(num))
      self.__clear_all()
      for i in range(len(t)):
        digit = int(str( t[len(t)-1-i] ))
        self.set_digit(7-i, digit)
    elif (num < 0) and (num >= -9999999):
      t = str(int(-num))
      self.__clear_all()
      for i in range(len(t)):
        digit = int(str( t[len(t)-1-i] ))
        self.set_digit(7-i, digit)
      self.__set_raw_value(0,64)
    else:
      self.__display_error()
    self.__send_buf()

  def float(self, num):
    """ Show float (ex: -3.1415) """
    self.__clear_all()
    number = str(num)
    dot_pos= number.find('.',0)
    sign = ( number[0] == '-')
    if dot_pos>=0:
      int_part = number[0:dot_pos]
      fract_part = number[dot_pos+1:]
    else:
      int_part = number
      fract_part = ''
      dot_pos = len(int_part)
    if sign:
      int_part = int_part[1:]
      dot_pos = dot_pos-1
    if len(int_part)>8:
      self.__display_error()
      return
    if sign and (len(int_part)>7):
      self.__display_error()
      return
    fract_part = fract_part+'0000'
    out = int_part + fract_part
    if sign:
      for i in range(1,8):
        self.set_digit(i, int(out[i-1]))
      self.__set_raw_value(0, 64)
      self.__set_dp(dot_pos)
    else:
      for i in range(8):
        self.set_digit(i, int(out[i]))
        self.__set_dp(dot_pos-1)
    self.__send_buf()

  def print( self, s, delay_ms=500 ):
    """ Print a string (as possible) and make it scrolling if longer than 4 bytes """
    def __print_for( sub_str ):
      for i in range( min(len(sub_str),8) ):
        self.__set_raw_value( pos=i, data=self.__alpha(sub_str[i]) )

    self.__clear_all()
    __print_for( s[0:0+8] )
    self.__send_buf()
    # scroll steps
    steps = len(s)-8
    if steps <= 0:
      return
    # Wait 4 time the scroll time before starting scrolling
    for i in range( 4 ):
		time.sleep_ms(delay_ms)

    for idx  in range( steps ):
      __print_for( s[idx+1:idx+1+8] )
      self.__send_buf()
      time.sleep_ms( delay_ms )

  def __clear_all(self):
    for i in range(15):
      self.dbuf[i] = 0x00

  def __digit(self,num):
    dig= [63, 6, 91, 79, 102, 109, 124, 7, 127, 103]
    return(dig[num%10])

  def __alpha(self,ch):
    """ return raw data corresponding to a char """
    _alpha = [119,124,88,94,121,113,103,118,6,14,0,56,55,84,92,115,103,80,109,49,62,28,0,0,110,91] # char from ASCII A(65) to ASCII(Z) 90
    _extra = [0,128,32] # Space(32), Point(46), Minus(45)

    if ch.isdigit():
      return self.__digit(int(ch))
    else:
      _ord = ord(ch)
      if _ord in (32, 46, 45): # Special case
        if _ord==32:
          return _extra[0] # space
        elif _ord==46:
          return _extra[1] # point
        elif _ord==45:
          return _extra[2] # Minus
      elif ch.isalpha():
        idx = ord(ch.upper())-65
        if idx < len(_alpha):
          return _alpha[idx]

    # Unknow char? --> Return a "SPACE"
    return 0

  def __set_raw_value(self, pos, data):
    # Set the 8bit data 0..255 @ position pos 0..7
    assert 0<=pos<=7, "invalid pos %s" % pos
    self.dbuf[pos*2] = int(data%256)

  def set_digit(self, pos, value):
    """ Set a given digit 0..9 at a given position 0..3. Requires display update() """
    self.__set_raw_value( pos, self.__digit(value%10) )

  def clear_digit(self, pos):
    """ Clear a given digit at position 0..3. Requires display update() """
    self.__set_raw_value( pos, data=0x00 )

  def __set_dp(self, pos):
    # set the decimal point
    self.dbuf[pos*2] = self.dbuf[pos*2] | 0x80

  def __clear_dp(self, pos):
    self.dbuf[pos*2] = self.dbuf[pos*2] & 0x7F

  def __send_buf(self):
    # Send the data buffer to the display
    self.i2c.writeto_mem( self.addr, VK16K33_DISP_DATA, self.dbuf)

  def __display_error(self):
    self.__clear_all()
    self.__set_raw_value(0,121)
    self.__set_raw_value(1,80)
    self.__set_raw_value(2,80)
    self.__send_buf()

  def clear(self):
    """ Clear the display """
    self.__clear_all()
    self.__send_buf()

  def __send_display( self ):
    """ send the Blink & Display config to the display """
    self.tbuf[0] = VK16K33_DISP_SETUP | self._display_status | self._blink_status
    self.i2c.writeto( self.addr , self.tbuf )

  def on(self):
    """ Set display on. """
    self._display_status = VK16K33_DISPLAY_ON
    self.__send_display()

  def off(self):
    """ Set display off. """
    self._display_status = VK16K33_DISPLAY_OFF
    self.__send_display()

  def blink_off(self):
    """ Set blink off. """
    self._blink_status = VK16K33_DISPLAY_OFF
    self.__send_display()

  def blink(self, freq ):
    """ Set up blink (1Hz=2, 2Hz=4, 0.5Hz=6). """
    assert freq in ( VK16K33_BLINK_1HZ, VK16K33_BLINK_2HZ, VK16K33_BLINK_0HZ5 )
    self._blink_status = freq
    self.__send_display()

  def brightness( self, value ):
    """ Brightness from 0 (min) to 15 (max) """
    assert 0<=value<=15
    self.tbuf[0] = VK16K33_DIM_SETUP + value
    self.i2c.writeto( self.addr, self.tbuf )
