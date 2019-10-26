# The MIT License (MIT)
#
# Copyright (c) 2019 Meurisse D for MCHobby.be
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
# Note:
# Code Ported from Arduino project  "Signal Generator with AD9833"
# from Cezar Chirila - contact@cezarchirila.com (published AllAboutCircutis.com )
import struct

SLEEP_NO_POWER_DOWN  = 0
SLEEP_DAC_POWER_DOWN = 1
SLEEP_CLOCK_DISABLED = 2 # Internal clock disabled
SLEEP_POWER_DOWN     = 3 # DAC & clock disabled

MODE_SINE     = 0 # Sine
MODE_TRIANGLE = 1 # triangle
MODE_CLOCK    = 2 # rectangle

class AD9833:
	""" Control the AD9833 signal generator (and its two frequency register). """
	def __init__( self, spi, fsync_pin, mclk=25000000 ):
		""" constructor.

		:param spi: must be initialized (in SPI in mode2 -> polarity=1, phase=0)
		:param fsync_pin: output pin for SPI transaction. Must be initialized HIGH.
		:param mclk freq: freq of the source clock (eg: 25000000 for 25 Mhz). """
		self.spi = spi
		self.fsync = fsync_pin # is the /SS from AD9833
		self.mclk = mclk

		self._freq  = 0 # current frequency
		self._phase = 0 # current phase
		self._mode  = MODE_SINE # current mode
		self._reset = False     # current reset state
		self._sleep = SLEEP_NO_POWER_DOWN # Generator is active

		self.controlRegister = 0x2000;  # Default control register : FREQ0, PHASE0, Sine
		self.fqRegister = 0x4000;       # Default frequency register is 0
		self.pRegister  = 0xC000;       # Default phase register is 0

	def write_data( self, value ):
		""" Send 16 bits data to the generator """
		# FSYNC pin must be pulled low when new data is received by AD9833
		self.fsync.value( 0 ) # FSYNC LOW)
		data = struct.pack( ">H", value )

		# SPI.transfer(highByte(data)); //  Send the first 8 MSBs of data
		# SPI.transfer(lowByte(data)); // Send the last 8 LSBs of data
		self.spi.write( data )
		# Set the FSYNC pin to high then end SPI transaction
		self.fsync.value( 1 )

	@property
	def freq( self ):
		""" Set the frequency selectect frequency registre. """
		return self._freq

	@freq.setter
	def freq( self, _freq ): # unsigned long _freq
		# First check that the data received is fine
		if _freq < 0:
			self._freq = 0
			freqReg = 0
		elif _freq > self.mclk:
			# If the frequency is more than maximum frequency, just set it to maximum
			self._freq = self.mclk / 2
			freqReg = pow(2, 28) - 1
		else:
			# If all is good, compute the freqReg knowhing that the analog output is
			# (mclk/2^28) * freqReg
			self._freq = _freq;
			freqReg = int(self._freq * (pow(2, 28) / self.mclk))

		# Initialise two variables that are 16bit long which we use to divide the
		# freqReg in two words
		# set D15 to 0 and D14 to 1 to put data in FREQ0/1 register
		MSW = (freqReg >> 14) | self.fqRegister # Take out the first 14bits
		# and set D15 to 0 and D14 to 1 or viceversa depending on FREQ reg
		LSW = (freqReg & 0x3FFF) | self.fqRegister
		# Send the data, most significant word first
		self.write_data( LSW )
		self.write_data( MSW )

	@property
	def phase( self ):
		""" Signal phase, between 0 and 4096 for 0 to 2*Pi """
		return self._phase

	@phase.setter
	def phase( self, _phase):
		""" Set the phase between 0 and 4096 """
		# Phase cannot be negative
		if _phase < 0:
			self._phase = 0
		elif _phase >= 4096:
			# Phase maximum is 2^12
			self._phase = 4096 - 1
		else:
			# If all is good, set the new phase value
			self._phase = _phase

		# Extract the 12 bits from the freqReg and set D15-1, D14-1, D13-0, D12-X to put data in PHASE0/1 register
		phaseData = self._phase | self.pRegister
		LSW = (self._phase & 0x3FFF) | self.pRegister
		self.write_data( phaseData )

	def write_ctrl_reg( self ):
		""" send the control register to AD9833 """
		self.write_data( self.controlRegister )

	@property
	def ctrl_reg( self ):
		""" Current control register """
		return self.controlRegister

	@ctrl_reg.setter
	def ctrl_reg( self, _controlRegister ):
		""" Update the control register to use """
		# Just make sure that the first two bits are set to 0
		self.controlRegister = _controlRegister & 0x3FFF
		self.write_ctrl_reg()

	@property
	def sleep( self ):
		""" Set the sleep mode with one of the SLEEP_xxx value """
		return self._sleep

	@sleep.setter
	def sleep( self, mode ):
		""" Set the sleep mode with one of the SLEEP_xxx value """
		self._sleep = mode
		if mode==SLEEP_NO_POWER_DOWN:
			self.controlRegister &= 0xFF3F # No power-down: D7-0 and D6-0
		elif mode==SLEEP_DAC_POWER_DOWN:
			self.controlRegister &= 0xFF7F # DAC powered down: D7-0 and D6-1
			self.controlRegister |= 0x0040
		elif mode==SLEEP_CLOCK_DISABLED:
			self.controlRegister &= 0xFFBF # Internal clock disabled: D7-1 and D6-0
			self.controlRegister |= 0x0080
		elif mode==SLEEP_POWER_DOWN:
			self.controlRegister |= 0x00C0 # Both DAC powered down and internal clock disabled
		else:
			raise ValueError( 'Invalid sleep mode %s' % mode )

		# Update the control register
		self.write_ctrl_reg()

	@property
	def reset( self ):
		""" Reset (HOLD) output to midscale (like disabling output) until reset is released.
		    Internal freq, phase & control register are left unchanged """
		return self._reset

	@reset.setter
	def reset( self,  value ):
		self._reset = value
		if value:
			self.controlRegister |= 0x0100  # Set D8 to 1. Internal registers reset, output disabled
		else:
			self.controlRegister &= 0xFEFF  # Set D8 to 0, not reset applied
		self.write_ctrl_reg()

	@property
	def mode( self ):
		""" Generator mode Sine, Triangle or clock (rectangle). See MODE_xxx constant """
		return self._mode

	@mode.setter
	def mode( self, value ):
		if value==MODE_SINE:
			self.controlRegister &= 0xFFDD # Output sine: D5-0 and D1-0
		elif value==MODE_TRIANGLE:
			self.controlRegister &= 0xFFDF # Output triangle: D5-0 and D1-1
			self.controlRegister |= 0x0002
		elif value==MODE_CLOCK:
			self.controlRegister &= 0xFFFD # Output clock (rectangle): D5-1 and D1-0
			self.controlRegister |= 0x0020

		self.write_ctrl_reg()

	def select_register( self, select ):
		""" Allow to select frequency register 0 or 1 to update. freq0 or freq1 """
		assert 0<=select<=1, "can only set to freq 0 or freq 1."
		if select==0:
			self.controlRegister &= 0xF3FF # Set D11 and D10 in control register to 0
			self.fqRegister = 0x4000 # Set D15 to 0 and D14 to 1 in a variable that will
			# later choose the FREQ0 register
			self.pRegister = 0xC000 # Set D15 to 1 and D14 to 1 and D13 to 0 for the PHASE register
		else:
			self.controlRegister |= 0x0C00 # Set D11 and D10 in control register to 1
			self.fqRegister = 0x8000 # Set D15 to 1 and D14 to 0 in a variable that will
 			# later choose the FREQ1 register
			self.pRegister = 0xD000 # Set D15 to 1 and D14 to 1 and D13 to 1 for the PHASE register
		self.write_ctrl_reg()
