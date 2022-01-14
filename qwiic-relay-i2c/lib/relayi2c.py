"""
relayi2c.py - I2C Qwiic Relay driver (COM-15093, SparkFun)
              I2C Qwiic Multi Relay driver (COM-16566, COM16810, KIT-16833, SparkFun)

* Author(s): Meurisse D., MCHobby (shop.mchobby.be).

Products:
---> Qwiic Single Relay    : https://www.sparkfun.com/products/15093
---> Qwiic Quad Relay      : https://www.sparkfun.com/products/16566
---> Qwiic Dual State Relay: https://www.sparkfun.com/products/16810
---> Qwiic Quad State Relay: https://www.sparkfun.com/products/16833
---> MicroMod RP2040 Processor : https://www.sparkfun.com/products/17720
---> MicroMod Machine Learning Carrier Board : https://www.sparkfun.com/products/16400

Remarks:
  Original product API is descrived here. Function name are almost identicals.
  https://github.com/sparkfun/SparkFun_Qwiic_Relay_Arduino_Library

------------------------------------------------------------------------

History:
  13 january 2022 - Dominique - initial portage from Arduino to MicroPython
"""

from micropython import const

__version__ = "0.0.1"

# RELAY_ONE   = 0x01,
# RELAY_TWO   = 0x02
# RELAY_THREE = 0x03
# RELAY_FOUR  = 0x04

# QUAD_RELAY_COMMANDS
TOGGLE_RELAY_ONE    = const(0x00+1)
TOGGLE_RELAY_TWO    = const(0x00+2)
TOGGLE_RELAY_THREE  = const(0x00+3)
TOGGLE_RELAY_FOUR   = const(0x00+4)
RELAY_ONE_STATUS    = const(0x04+1)
RELAY_TWO_STATUS    = const(0x04+2)
RELAY_THREE_STATUS  = const(0x04+3)
RELAY_FOUR_STATUS   = const(0x04+4)
TURN_ALL_OFF        = const(0x0A)
TURN_ALL_ON         = const(0x0B)
TOGGLE_ALL          = const(0x0C)
RELAY_ONE_PWM       = const(0x0F+1) # 0x10
RELAY_TWO_PWM       = const(0x0F+2) # 0x10
RELAY_THREE_PWM     = const(0x0F+3) # 0x10
RELAY_FOUR_PWM      = const(0x0F+4) # 0x10

# QUAD_RELAY_STATUS
QUAD_RELAY_OFF      = const(0)
QUAD_RELAY_ON       = const(15)

# SINGLE_RELAY_COMMANDS
TURN_RELAY_OFF      = const(0x00)
TURN_RELAY_ON       = const(0x01)
FIRMWARE_VERSION    = const(0x04)
MYSTATUS            = const(0x05)

# SINGLE_RELAY_STATUS
SINGLE_RELAY_OFF    = const(0x00)
SING_RELAY_ON       = const(0x01)

QUAD_DEFAULT_ADDRESS   = const(0x6D) # alternate 0x6C
SINGLE_DEFAULT_ADDRESS = const(0x18) # alternate 0x19

QUAD_SSR_DEFAULT_ADDRESS = const( 0x08 ) # alternate 0x09
DUAL_SSR_DEFAULT_ADDRESS = const( 0x0A ) # alternate 0x0B

ADDRESS_LOCATION = const( 0xC7 ) # Change module address
# INCORR_PARAM     0xFF

class BaseRelay():
	def __init__( self, i2c, address ):
		self.address = address
		self.i2c = i2c
		self.buf1 = bytearray(1)
		self.buf2 = bytearray(2)

	@property
	def version( self ):
		self.buf1[0] = FIRMWARE_VERSION
		self.i2c.writeto( self.address, self.buf1  )

		self.i2c.readfrom_into( self.address, self.buf2 )
		return self.buf1[0] + ( float(self.buf2[1]) / 10 )

	def read_reg( self, reg ):
		self.buf1[0] = reg
		self.i2c.writeto( self.address, self.buf1 )
		self.i2c.readfrom_into( self.address, self.buf1 )
		return self.buf1[0]

	def write_reg( self, reg, value ):
		self.buf1[0] = value
		self.i2c.writeto_mem( self.address, reg, self.buf1 )

	def change_address( self, new_addr ):
		assert 0x07 <= new_addr <= 0x78, "Address range must be in 0x07..0x78"
		self.buf1[0] = ADDRESS_LOCATION
		self.i2c.writeto( self.address, self.buf1 )
		self.buf1[0] = new_addr
		self.i2c.writeto( self.address, self.buf1 )


class SingleRelay( BaseRelay ):
	""" Handling the Qwiic Single Relay (SparFun, COM-15093)"""
	def __init__( self, i2c, address=SINGLE_DEFAULT_ADDRESS ):
		super().__init__( i2c, address )

	def value( self, state=None ):
		""" Set the relay state (mimic Pin class) """
		if state==None:
			return self.state
		else:
			self.buf1[0] = TURN_RELAY_ON if state else TURN_RELAY_OFF
			self.i2c.writeto( self.address, self.buf1 )

	def on( self ):
		self.value( True )

	def off( self ):
		self.value( False )

	def toggle( self ):
		self.value( False if self.state else True )

	@property
	def state( self ):
		return self.read_reg(MYSTATUS) > 0

class MultiRelay( BaseRelay ):
	""" Handling the Qwiic Multiple Relay/SSR (SparFun, COM-16566, COM16810, KIT-16833) """
	def __init__( self, i2c, address ):
		super().__init__( i2c, address )

	def value( self, relay, state=None ):
		""" Set the relay state (mimic Pin class) """
		if state==None:
			return self.state( relay )
		else:
			if state != self.state( relay ): # requested state <> actual relay state
				self.buf1[0] = 0x00+relay # TOGGLE_RELAY_ONE, _TWO, ....
				self.i2c.writeto( self.address, self.buf1 )

	def on( self, relay ):
		self.value( relay, True )

	def off( self, relay ):
		self.value( relay, False )

	def toggle( self, relay ):
		self.buf1[0] = 0x00+relay # TOGGLE_RELAY_ONE, _TWO, ....
		self.i2c.writeto( self.address, self.buf1 )

	def state( self, relay ):
		# 0x04+relay : RELAY_ONE_STATUS, RELAY_TWO_STATUS, ...
		return self.read_reg(0x04+relay) > 0

	def slow_pwm( self, relay, duty=None ):
		# Read or Set slow PWM.
		# Manage slow PWM (1Hz) with a range from 0-100 so as this is the maximum PWM resolution for Zero-crossing SSR's at 50Hz
		if duty==None:
			self.read_reg( 0x0F+relay ) # RELAY_ONE_PWM, RELAY_TWO_PWM, ...
		else:
			assert 0<= duty <=100, "Duty must be in range 0..100"
			self.write_reg( 0x0F+relay, duty )

	def toggle_all( self ):
		# See for more
		self.buf1[0] = TOGGLE_ALL
		self.i2c.writeto( self.address, self.buf1 )

	def on_all( self ):
		# See for more
		self.buf1[0] = TURN_ALL_ON
		self.i2c.writeto( self.address, self.buf1 )

	def off_all( self ):
		# See for more
		self.buf1[0] = TURN_ALL_OFF
		self.i2c.writeto( self.address, self.buf1 )
