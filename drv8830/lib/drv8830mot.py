# drv8830mot - MicroPython library to support MiniMoto I2C Driver / Mini I2C
#      motor driver based on DRV8830 low voltage motor controler.
#
# Copyright (c) 2019 Meurisse D. for MCHobby.be - portage to MicroPython.
# Copyright (c) 17 Sep 2013- Mike Hord, SparkFun Electronics - Arduino Library
#
# Keeping the original license:
#     This code is beerware; if you use it, please buy me (or any other
#    SparkFun employee) a cold beverage next time you run into one of
#    us at the local.
#
# Based on https://github.com/Seeed-Studio/Drv8830_Motor_Driver
#
from micropython import const
I2C_READ   = const( 0x01 ) # I2C read bit set
# Some values we'll load into TWCR a lot
START_COND = const( 0xA4 ) # (1<<TWINT) | (1<<TWSTA) | (1<<TWEN)
STOP_COND  = const( 0x94 ) # (1<<TWINT) | (1<<TWSTO) | (1<<TWEN)
CLEAR_TWINT= const( 0x84 ) # (1<<TWINT) | (1<<TWEN)
NEXT_BYTE  = const( 0xC4 ) # (1<<TWINT) | (1<<TWEA) | (1<<TWEN)

# Fault constants
FAULT  = const( 0x01 )
ILIMIT = const( 0x10 )
OTS    = const( 0x08 )
UVLO   = const( 0x04 )
OCP    = const( 0x02 )

class DRV8830:
	def __init__(self, i2c, address=0xD0 ):
		self.i2c = i2c
		self.address = address
		self.buf1 = bytearray(1)

	def drive(self, speed ):
		""" Set speed from -63 to +63. """
		assert -63 <= speed <= 63, "Speed must be in range -63..63"
		# clear the fault status
		self.buf1[0] = 0x80
		self.i2c.writeto_mem( self.address, 0x01, self.buf1 )

		# Write speed
		self.buf1[0] = abs(speed) # Absolute value
		self.buf1[0] = self.buf1[0] << 2 # make room for bits 1:0
		# Set bit 1:0 depending on speed sign
		if speed < 0:
			self.buf1[0] = self.buf1[0] | 0x01
		else:
			self.buf1[0] = self.buf1[0] | 0x02

		self.i2c.writeto_mem( self.address, 0x00, self.buf1 )


	def stop(self):
		""" Stop motor propeling """
		self.buf1[0] = 0x00
		self.i2c.writeto_mem( self.address, 0x00, self.buf1 )

	def brake(self):
		""" Provide a heavy load to the motor (to slow it down) """
		self.buf1[0] = 0x03
		self.i2c.writeto_mem( self.address, 0x00, self.buf1 )

	@property
	def fault(self):
		self.buf1[0] = 0x00
		self.i2c.readfrom_mem_into( self.address, 0x01, self.buf1 )
		_r = self.buf1[0]
		self.buf1[0] = 0x80 # clear fault
		self.i2c.writeto_mem( self.address, 0x01, self.buf1 )
		return _r
