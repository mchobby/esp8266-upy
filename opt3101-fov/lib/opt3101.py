"""
opt3101.py : MicroPython driver for 3-Channel Wide FOV Time-of-Flight
             Distance Sensor Using OPT3101.
* Author(s):
   23 may 2021: Meurisse D. (shop.mchobby.be) - port to MicroPython
				https://github.com/pololu/opt3101-arduino (including docs)
"""

__version__ = "0.0.1.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/opt3101-fov"

from micropython import const
import time
import struct

BRIGHTNESS_LOW = const(0)
BRIGHTNESS_HIGH = const(1)
BRIGHTNESS_ADAPTIVE = const(255)

CHANNEL_AUTO_SWITCH = const(255)

REG80_DEFAULT = const(0x4E1E)

class OPT3101:
	def __init__( self, i2c, address=0x58 ):
		self.i2c = i2c
		self.address = address

		self.channel_used = 0 #uint8_t
		self.brightness_used = BRIGHTNESS_LOW
		self.ambient = 0 # int16_t
		self.temperature = 0 # int16_t
		self._i = 0 # int32_t
		self._q = 0 # int32_t
		self.amplitude = 0 # uint16_t
		self.phase = 0 # int16_t SIGNED!
		self.distance = 0 # int16_t was distanceMillimeter
		self.buf3 = bytearray(3)
		self.buf6 = bytearray(6)

		self.__timing_generator_enabled = False
		self.__start_sample_ms = 0
		self.__frame_delay_ms = 0

		# Init() implementation
		self.reset_and_wait()
		self.configure_default()

	def configure_default( self ):
		self.write_reg32(0x89, 7000) # TG_OVL_WINDOW_START = 7000
		self.write_reg32(0x6e, 0x0a0000) # EN_TEMP_CONV = 1
		self.write_reg32(0x50, 0x200101) # CLIP_MODE_FC = 1, CLIP_MODE_TEMP = 0, CLIP_MODE_OFFSET = 0
		# IQ_READ_DATA_SEL = 2: This lets us read "raw" IQ values later.
		reg2e = self.read_reg32( 0x2e )
		# reg2e = (reg2e & ~((uint32_t)7 << 9)) | (2 << 9);
		#                &  ( 0xFFFFFFFF ^ ((7 << 9)|(2<<9)) )
		reg2e = (reg2e & ( 0xFFFFFF ^ (7 << 9))) | (2<<9)
		self.write_reg32( 0x2e, reg2e )

		self.set_monoshot_mode()
		self.set_frame_timing(512)

	def reset_and_wait( self ):
		# Set SOFTWARE_RESET to 1, but don't use writeReg, because the OPT3101 will
		# stop acknowledging after it receives the first register value byte.
		try:
			self.buf2[0] = 1 # LSB first
			self.buf2[1] = 0
			self.i2c.writeto( self.address, self.buf2 )
		except:
			pass

		time.sleep_ms(50)

		# Wait for INIT_LOAD_DONE to be set, indicating that the OPT3101 is done
		# loading settings from its EEPROM.
		while (self.read_reg32(3) & 0x100) != 0x100: # test the 8th bit
			time.sleep_ms(1)


	def write_reg32( self, reg, value32 ): # Value is uint32
		self.buf3[0] = value32 & 0xFF      # send lower bits first
		self.buf3[1] = (value32>>8) & 0xFF
		self.buf3[2] = (value32>>16) & 0xFF

		self.i2c.writeto_mem( self.address, reg, self.buf3 )

	def read_reg32( self, reg ):
		# Apparently, we can read 6 bytes from the registers
		# self.i2c.readfrom_mem_into( self.address, reg, self.buf6 )
		# return self.buf6[3] + (self.buf6[4]<<8) + (self.buf6[5]<<16)
		self.i2c.readfrom_mem_into( self.address, reg, self.buf3 )
		return self.buf3[0] + (self.buf3[1]<<8) + (self.buf3[2]<<16)

	def set_frame_timing( self, subFrameCount ):
		def is_pow_of_two( i ):
			return (i & (i-1))==0
		# Make sure subFrameCount is a power of 2 between 1 and 4096.
		if not(1 <= subFrameCount <= 4096) or not is_pow_of_two(subFrameCount):
			subFrameCount = 4096


		# Implement equation 6 from sbau310.pdf to calculate XTALK_FILT_TIME CONST, but without floating-point operations.
		timeConst = 0 #
		while (subFrameCount << timeConst) < 1024:
			timeConst += 1

		reg2e = self.read_reg32( 0x2e ) # uint32
		# reg2e = reg2e & ~(uint32_t)0xF00000 | (uint32_t)timeConst << 20;
		reg2e = reg2e &  (0xFFFFFF ^ 0xF00000) | ((timeConst << 20) & 0xFFFFFF)
		self.write_reg32( 0x2e, reg2e )
		# Set NUM_SUB_FRAMES and NUM_AVG_SUB_FRAMES.
		#    (subFrameCount - 1) | (uint32_t)(subFrameCount - 1) << 12
		self.write_reg32( 0x9f, (subFrameCount - 1) | (((subFrameCount - 1) << 12) & 0xFFFFFF) )
		# Set TG_SEQ_INT_MASK_START and TG_SEQ_INT_MASK_END according to what
		# the OPT3101 datasheet says, but it's probably not needed.
		#    (subFrameCount - 1) | (uint32_t)(subFrameCount - 1) << 12
		self.write_reg32( 0x97, (subFrameCount - 1) | (((subFrameCount - 1) << 12) & 0xFFFFFF) )

		# Assuming that SUB_VD_CLK_CNT has not been changed, each sub-frame is 0.25 ms.
		# The +3 is to make sure we round up.
		frameTimeMs = int((subFrameCount + 3) / 4)

		# Add a ~6% margin in case the OPT3101 clock is running faster.
		self.__frame_delay_ms = int(frameTimeMs + (frameTimeMs + 15) / 16)


	def set_channel(self, channel):
		if channel > 2:
			channel = CHANNEL_AUTO_SWITCH

		reg2a = self.read_reg32( 0x2a )

		if channel == CHANNEL_AUTO_SWITCH:
			reg2a = reg2a | (1 << 0) # EN_TX_SWITCH = 1
		else:
			# reg2a = reg2a & ~((uint32_t)1 << 0)
			reg2a = reg2a & (0xFFFFFF^(1 << 0))  # EN_TX_SWITCH = 0
			reg2a = reg2a & (0xFFFFFF^(3 << 1)) | ((channel & 3) << 1)

		self.write_reg32( 0x2a, reg2a )


	def next_channel(self):
		next = self.channel_used + 1
		if next > 2:
			next = 0
		self.set_channel( next )


	def set_brightness(self, brightness):
		reg2a = self.read_reg32( 0x2a )

		if brightness == BRIGHTNESS_ADAPTIVE:
			reg2a = reg2a | (1 << 15) # EN_ADAPTIVE_HDR = 1
		else:
			# EN_ADAPTIVE_HDR = 0, SEL_HDR_MODE = hdr
			# reg2a = reg2a & ~(uint32_t)0x18000 | ((uint32_t)br & 1) << 16;
			reg2a = reg2a & (0xFFFFFF ^ 0x18000) | ((brightness & 1) << 16)

		self.write_reg32( 0x2a, reg2a )


	def set_continuous_mode(self):
		# MONOSHOT_FZ_CLKCNT = default, MONOSHOT_NUMFRAME = 1, MONOSHOT_MODE = 0
		self.write_reg32( 0x27, 0x26AC04 )


	def set_monoshot_mode(self):
		# MONOSHOT_FZ_CLKCNT = default, MONOSHOT_NUMFRAME = 1, MONOSHOT_MODE = 3
		self.write_reg32( 0x27, 0x26ac07)
		# DIS_GLB_PD_OSC = 1, DIS_GLB_PD_AMB_DAC = 1, DIS_GLB_PD_REFSYS = 1, (other fields default)
		self.write_reg32(0x76, 0x000121 )
		# POWERUP_DELAY = 95
		self.write_reg32( 0x26, (95 << 10)|0xF )


	def enable_timing_generator(self, enabled ):
		if enabled:
			self.write_reg32( 0x80, REG80_DEFAULT | 1 ) # TG_EN = 1
		else:
			self.write_reg32( 0x80, REG80_DEFAULT ) # TG_EN = 0
		self.__timing_generator_enabled = enabled


	def enable_data_ready_output(self, gpPin ):
		assert 1 <= gpPin <= 2, "only pin 1 or 2!"

		# DIG_GPO_SEL0 = 9 (DATA_RDY)
		reg0b = self.read_reg32( 0x0b )
		# reg0b = (reg0b & ~(uint32_t)0xF) | 9;
		reg0b = (reg0b & (0xFFFFFFFF^0xF)) | 9
		self.write_reg32( 0x0b, reg0b )

		reg78 = self.read_reg32( 0x78 )
		if gpPin==1:
			# GPO1_MUX_SEL = 2 (DIG_GPO_0), GPIO1_OBUF_EN = 1
			# reg78 = (reg78 & ~((uint32_t)7 << 6)) | (2 << 6) | (1 << 12);
			reg78 = (reg78 & (0xFFFFFFFF^(7 << 6))) | (2 << 6) | (1 << 12)
		elif gpPin==2:
			# GPO2_MUX_SEL = 2 (DIG_GPO_0), GPIO2_OBUF_EN = 1
			# reg78 = (reg78 & ~((uint32_t)7 << 9)) | (2 << 9) | ((uint16_t)1 << 15);
			reg78 = (reg78 & (0xFFFFFFFF^(7 << 9))) | (2 << 9) | (1 << 15)
		self.write_reg32( 0x78, reg78 )


	def start_sample(self):
		if not self.__timing_generator_enabled:
			self.enable_timing_generator( enabled=True )
		# Set MONOSHOT_BIT to 0 before setting it to 1, as recommended here:
		# https://e2e.ti.com/support/sensors/f/1023/p/756598/2825649#2825649
		self.write_reg32( 0x00, 0x000000 )
		self.write_reg32( 0x00, 0x800000 )
		self.__start_sample_ms = time.ticks_ms()

	def is_sample_done(self):
		return (time.ticks_ms() - self.__start_sample_ms) > self.__frame_delay_ms

	def read_output_regs( self ):
		reg08 = self.read_reg32( 0x08 )
		reg09 = self.read_reg32( 0x09 )
		reg0a = self.read_reg32( 0x0a )

		self.channel_used = (reg08 >> 18) & 3
		if self.channel_used > 2:
			self.channel_used = 2
		self.brightness_used = (reg08 >> 17) & 1

		self._i = self.read_reg32( 0x3b ) # IPhase_XTALK_INT_REG
		if self._i > 0x7fffff :
			self._i -= 0x1000000
		self._q = self.read_reg32( 0x3c ) # IPhase_XTALK_INT_REG
		if self._q > 0x7fffff:
			self._q -= 0x1000000

		self.amplitude = reg09 & 0xFFFF # AMP_OUT
		# 16 bits should be signed value --> restransform it into signed result
		self.phase = struct.unpack( ">h", struct.pack(">H", reg08 & 0xFFFF))[0] # PHASE_OUT

		# c / (2 * 10 MHz * 0x10000) = 0.22872349395 mm ~= 14990/0x10000
		self.distance = (14990.0 * self.phase) / 0x10000 # >> 16
		self.ambient = (reg0a >> 2) & 0x3FF # AMB_DATA
		self.temperature = (reg0a >> 12) & 0xFFF # TMAIN

	def sample(self):
		self.start_sample()
		time.sleep_ms( self.__frame_delay_ms )
		self.read_output_regs()
