"""
rs485iso.py is a micropython module for the Olimex MOD-RS485-ISO board.

It allows the user to interact with RS485 bus through I2C / UART connexion

MOD-RS485-ISO board : http://shop.mchobby.be/product.php?id_product=1414
MOD-RS485-ISO board : https://www.olimex.com/Products/Modules/Interface/MOD-RS485-ISO/open-source-hardware
User Guide : https://www.olimex.com/Products/Modules/LCD/MOD-LCD-1x9/resources/LCD1X9.pdf

Meurisse D. - oct 3, 2021 - Ported to MicroPython from RS485ISO.cpp - support@mchobby.be
							Based on RS485ISO.cpp, original work from Stefan Mavrodiev from OLIMEX LTD <support@olimex.com> in 2013

----------------------------------------------------------------------
  GNU GENERAL PUBLIC LICENSE

 This program is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 2 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program; if not, write to the Free Software
 Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
 MA 02110-1301, USA.
"""
from micropython import const

# Define read-only registers
REGISTER_ID = const(0x20)
REGISTER_FW = const(0x21)
# Define read/write registers
REGISTER_ADDR = const(0x22)
REGISTER_MODE = const(0x23)
REGISTER_CTRL = const(0x24)
REGISTER_BR   = const(0x25)

REGISTER_TX  = const(0x26)
REGISTER_RX  = const(0x27)


TX_ENABLED   = const(1 << 1)
TX_DISABLED  = const(0 << 1)
RX_ENABLED   = const(1 << 0)
RX_DISABLED  = const(0 << 0)

PASS_MODE    = const(0x00) # Pass mode - Signals on TX line pass straigth throw the device and are transmitted to RS-485 line. The same apply to the RX.
BRIDGE_MODE  = const(0x01) # Bridge mode - TX and RX are disabled. Data can be send via I2C bus.

UART_B50      = const(0)
UART_B75      = const(1)
UART_B110     = const(2)
UART_B134     = const(3)
UART_B150     = const(4)
UART_B300     = const(5)
UART_B600     = const(6)
UART_B1200    = const(7)
UART_B1800    = const(8)
UART_B2400    = const(9)
UART_B4800    = const(10)
UART_B7200    = const(11)
UART_B9600    = const(12)
UART_B14400   = const(13)
UART_B19200   = const(14)
UART_B38400   = const(15)
UART_B57600   = const(16)
UART_B76800   = const(17)
UART_B115200  = const(18)
UART_B128000  = const(19)
UART_B230400  = const(20)
UART_B500000  = const(21)
UART_B576000  = const(22)
UART_B1000000 = const(23)

class RS485ISO:
	def __init__( self, i2c, address=0x22 ):
		self.i2c = i2c
		self.address = address
		self.buf1 = bytearray(1)

	@property
	def device_id( self ):
		""" identification of device """
		self.i2c.readfrom_mem_into( self.address, REGISTER_ID, self.buf1)
		return self.buf1[0]

	@property
	def version( self ):
		""" Firmware version """
		self.i2c.readfrom_mem_into( self.address, REGISTER_FW, self.buf1)
		return self.buf1[0]

	@property
	def mode( self ):
		""" Communication mode with RS485 bus (Pass or Bridge)"""
		self.i2c.readfrom_mem_into( self.address, REGISTER_MODE, self.buf1 )
		return self.buf1[0]

	@mode.setter
	def mode( self, value ):
		assert value in (PASS_MODE, BRIDGE_MODE), "Invalid mode %s" % value
		self.buf1[0] = value
		self.i2c.writeto_mem( self.address, REGISTER_MODE, self.buf1 )

	@property
	def control( self ):
		""" Enable RX / TX data flow """
		self.i2c.readfrom_mem_into( self.address, REGISTER_CTRL, self.buf1 )
		return self.buf1[0]

	@control.setter
	def control( self, value ):
		# Combination of TX_ENABLED, TX_DISABLED, RX_ENABLED, RX_DISABLED
		self.buf1[0] = value
		self.i2c.writeto_mem( self.address, REGISTER_CTRL, self.buf1 )

	@property
	def baud_rate( self ):
		# return one of the UART_Bxxx value
		self.i2c.readfrom_mem_into( self.address, REGISTER_BR, self.buf1 )
		return self.buf1[0]

	@baud_rate.setter
	def baud_rate( self, value ):
		self.buf1[0] = value
		self.i2c.writeto_mem( self.address, REGISTER_BR, self.buf1 )

#void setAddress(uint8_t address);

	def send( self, buffer ):
		""" Send the data buffer over I2C to the RS485 bus (must be in bridged mode) """
		for ch in buffer:
			self.buf1[0] = ch
			self.i2c.writeto_mem( self.address, REGISTER_TX, self.buf1 )

	def read( self, data, max_read=None ):
		""" Fills the buffer with received data. Returns when the buffer is
		    filled """
		if max_read==None:
			max_read = len(data)
		for idx in range( max_read ):
			self.i2c.readfrom_mem_into( self.address, REGISTER_RX, self.buf1 )
			data[idx] = self.buf1[0]


#void readData(uint8_t *data, uint8_t length);
