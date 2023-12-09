# stonatm@gmail.com
# Gravity DFRobot DFR0645-R DFR0645-G
# TM1650 4 digit 8 segment led display
# i2c software implementation
# esp32 micropython driver
"""
4-Digital LED segment display module (DFR0645)
==============================================

MicroPython library to support DFR0645 digital display from DFRobot.
I2C bus at 100 KHz max

DFR0645 - 4-Digital LED segment display module V1.0
  <https://www.dfrobot.com/product-1967.html> (Product ID: DFR0645)

History
-------
Dec 7, 2023 - Meurisse D. - make it hardware Agnostic (like other libs of esp8266-upy)
								reduce method name
								brightness control
								print string with scrolling

Dec 6, 2022 - Dawid Stankiewicz (stonatm) - initial portage for MicroPython on ESP32
		Awesome work of 118 lines made on TM1650 driver
		https://github.com/stonatm/tm1650_micropython

"""
import time

class LedSegment4():
  """ TM1650 4-Digital LED Segment Display module (DFR0645) driver for MicroPython"""

  def __init__(self, i2c, addr=0x48 ):
    self.dbuf = bytearray(4)
    self.tbuf = bytearray(1)
    self.i2c  = i2c
    self.addr = (addr>>1) # Led address = 0x24
    self.on()

  def __clear_all(self):
    self.tbuf[0] = 0
    for i in range(4):
      self.dbuf[i] = self.tbuf[0]

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


  def __set_raw_value(self, pos, value):
    self.tbuf[0] = int(value%256)
    self.dbuf[pos%4] = self.tbuf[0]

  def __set_dp(self, pos):
    self.tbuf[0] = self.dbuf[pos%4]|0x80
    self.dbuf[pos%4] = self.tbuf[0]

  def __clear_dp(self, pos):
    self.tbuf[0] = self.dbuf[pos%4]&0x7f
    self.dbuf[pos%4] = self.tbuf[0]

  def __send_buf(self):
    for i in range(4):
      self.tbuf[0] = self.dbuf[i]
      self.i2c.writeto(self.addr+0x10+i, self.tbuf) # 0x34+i = ledAddr + 0x10 + i = 0x24 + 0x10 + i

  def __display_error(self):
    self.__clear_all()
    self.__set_raw_value(0,121)
    self.__set_raw_value(1,80)
    self.__set_raw_value(2,80)
    self.__send_buf()

  def print( self, s, delay_ms=500 ):
    """ Print a string (as possible) and make it scrolling if longer than 4 bytes """
    def __print_for( sub_str ):
      for i in range( min(len(sub_str),4) ):
        self.__set_raw_value( pos=i, value=self.__alpha(sub_str[i]) )

    self.__clear_all()
    __print_for( s[0:0+4] )
    self.__send_buf()
    # scroll steps
    steps = len(s)-4
    if steps <= 0:
      return
    # Wait 4 time the scroll time before starting scrolling
    for i in range( 4 ):
		time.sleep_ms(delay_ms)

    for idx  in range( steps ):
      __print_for( s[idx+1:idx+1+4] )
      self.__send_buf()
      time.sleep_ms( delay_ms )

  def int(self, num):
    """ Show integer (9999 to -9999) """
    if (num >= 0) and (num <= 9999):
      t = str(int(num))
      self.__clear_all()
      for i in range(len(t)):
        digit = int(str( t[len(t)-1-i] ))
        self.set_digit(3-i, digit)
    elif (num < 0) and (num >= -999):
      t = str(int(-num))
      self.__clear_all()
      for i in range(len(t)):
        digit = int(str( t[len(t)-1-i] ))
        self.set_digit(3-i, digit)
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
    if len(int_part)>4:
      self.__display_error()
      return
    if sign and (len(int_part)>3):
      self.__display_error()
      return
    fract_part = fract_part+'0000'
    out = int_part + fract_part
    if sign:
      for i in range(1,4):
        self.set_digit(i, int(out[i-1]))
      self.__set_raw_value(0, 64)
      self.__set_dp(dot_pos)
    else:
      for i in range(4):
        self.set_digit(i, int(out[i]))
        self.__set_dp(dot_pos-1)
    self.__send_buf()

  def clear(self):
    """ Clear the display """
    self.__clear_all()
    self.__send_buf()

  def on(self):
    """ Set display on. """
    self.i2c.writeto( self.addr , b'0x81')

  def off(self):
    """ Set display off. """
    self.i2c.writeto( self.addr, b'0x80')

  def brightness( self, value ):
    """ Set the brightness 0=min, 7=max """
    assert 0<=value<=7
    # TM6150 brightness: 0=Max, 1=Min, 7=Just before max
    # reorder to logical 0=min_bright to 7=max_bright
    if value==7:
        value=0 # the max for LCD
    else:
        value += 1
    #i2cWriteCmd((brightnessValue<<4)|0x01);
    self.i2c.writeto( self.addr, bytearray([ (value<<4)|0x01 ]) )


  def set_digit(self, pos, value):
    """ Set a given digit 0..9 at a given position 0..3. Requires display update() """
    self.tbuf[0] = self.__digit(value%10)
    self.dbuf[pos%4] = self.tbuf[0]

  def clear_digit(self, pos):
    """ Clear a given digit at position 0..3. Requires display update() """
    self.tbuf[0] = 0
    self.dbuf[pos%4] = self.tbuf[0]
