""" vcnl4035.py - library for Vishay VCNL4035 Proximity sensor for MicroPython

   REQUIRES breakout board must HAVE VCNL4035 + 3x IR LEDs in order to detect SWIPES

* Source   :  https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be).

11 Apr 2026 - domeu -creation

 remarks: 
   based on work Vishay_VCNL4035_Arduino from LukeYoung3000
   available at https://github.com/LukeYoung3000/Vishay_VCNL4035_Arduino/blob/master/VCNL4035_Lib_Hardware.cpp
"""
from machine import Pin
from vcnldefs import *
import struct, time

irq_count = 0
irq_check = None # last time it has been checked
def irq_cb( pin ):
	global irq_count
	irq_count += 1
	# print( "------ IRQ" )

class VCNL4035():
	""" Driver class for VCNL4035 proximity sensor """

	def __init__( self, i2c, address=0x60, mode=VCNL4035_MODES.PROXIMITY ):
		""" :param mode: one of the VCNL4035_MODES constant """
		self.i2c = i2c
		self.addr = address
		self.buf2 = bytearray( 2 )
		self.buf6 = bytearray( 6 )
		self.int_pin = None # Interrupt Pin. see set_int_pin()

		# Proximity/Gesture Mode Settings
		self.gesture_mode = ps_settings_t() # default are zeroed (0)
		self.ps_mode = ps_settings_t() # default are zeroed (0)


		# Gesture Mode Default Settings
		self.gesture_mode.ps_conf_1.ps_it = VCNL4035_PS_IT.PS_IT_50us
		self.gesture_mode.ps_conf_2.ps_hd = VCNL4035_PS_HD.PS_HD_16_BIT
		self.gesture_mode.ps_conf_2.gesture_mode = VCNL4035_GESTURE_MODE.GESTURE_MODE_ENABLE
		self.gesture_mode.ps_conf_2.gesture_int_en = VCNL4035_GESTURE_INT_EN.GESTURE_INT_EN_ENABLE
		self.gesture_mode.ps_conf_3.ps_af = VCNL4035_PS_AF.PS_AF_ON
		self.gesture_mode.ps_ms.led_i = VCNL4035_LED_I.LED_I_50mA
		self.gesture_mode.ps_thdl = 0
		self.gesture_mode.ps_thdh = 0xffff

		# Proximity Mode Default Settings
		self.ps_mode.ps_conf_1.ps_it = VCNL4035_PS_IT.PS_IT_50us
		self.ps_mode.ps_conf_1.ps_pers = VCNL4035_PS_PERS.PS_PERS_4_READING
		self.ps_mode.ps_conf_1.ps_duty = VCNL4035_PS_DUTY.PS_DUTY_1_320
		self.ps_mode.ps_conf_2.ps_int = VCNL4035_PS_INT.PS_INT_CLOSING
		self.ps_mode.ps_conf_2.ps_ns = VCNL4035_PS_NS.PS_NS_TWO_STEP_MODE_TIMES_1
		self.ps_mode.ps_conf_2.ps_hd = VCNL4035_PS_HD.PS_HD_16_BIT
		self.ps_mode.ps_conf_2.ps_gain = VCNL4035_PS_GAIN.PS_GAIN_TWO_STEP_MODE
		self.ps_mode.ps_conf_3.ired_select = VCNL4035_IRED_SELECT.IRED_SELECT_1
		self.ps_mode.ps_ms.led_i = VCNL4035_LED_I.LED_I_50mA
		self.ps_mode.ps_ms.ps_sc_cur = VCNL4035_PS_SC_CUR.PS_SC_CUR_TYPICAL_TIMES_1
		self.ps_mode.ps_thdl = 15
		self.ps_mode.ps_thdh = 50

		self.init( mode )

	def init( self, mode ):
		""" configure the remote component.
		    :param mode: one of VCNL4035_MODES.xxx constant  """
		# Equivalent of void init( lide )
		if mode==VCNL4035_MODES.GESTURE:
			#self.__setGestureMode()
			self.__updatePsSettings(self.gesture_mode)
		elif mode==VCNL4035_MODES.PROXIMITY:
			#self.__setPSMode()
			self.__updatePsSettings(self.ps_mode)
		else:
			# AMBIENT_LIGHT_SENSOR
			#self.setPSMode()
			self.__updatePsSettings(self.ps_mode)

	def write_reg( self, reg, low_byte, high_byte ):
		self.buf2[0]=low_byte
		self.buf2[1]=high_byte
		self.i2c.writeto_mem( self.addr, reg, self.buf2 )

	def read_reg( self, reg ):
		self.i2c.readfrom_mem_into( self.addr, reg, self.buf2 )
		return struct.unpack( '<H', self.buf2 )[0]

	def write_reg_bits( self, reg, msb_lsb, start_bit, end_bit, val ):
		assert (end_bit-start_bit)>=0
		# read current value (uint16)
		current_val = self.read_reg( reg )
		# create bit mask (uint16)
		mask = 0
		for i in range( start_bit, end_bit+1): # start_bit..end_bit
			mask += (1 << i)
		# shift the val to the required bit range
		value = mask & (val << start_bit )
		# Shift mask & value to right position in 16bit range
		if msb_lsb:
			mask = mask << 8
			value = value << 8
		# create new register value
		new_val = 0
		new_val = current_val & (0xFFFF^mask)
		new_val += value
		# getting high & low bytes
		low = new_val & 0xFF
		high = new_val >> 8
		# Update register
		self.write_reg( reg, low, high )

	def __updatePsSettings( self, _set ):
		# :param _set: ps_setting_t

		# PS_CONF_1 (all uint8)
		ps_sd   = (_set.ps_conf_1.ps_sd << VCNL4035_PS_CONF_1.PS_SD)
		ps_it   = (_set.ps_conf_1.ps_it << VCNL4035_PS_CONF_1.PS_IT_START)
		ps_pers = (_set.ps_conf_1.ps_pers << VCNL4035_PS_CONF_1.PS_PRES_START)
		ps_duty = (_set.ps_conf_1.ps_duty << VCNL4035_PS_CONF_1.PS_DUTY_START)
		ps_conf_1 = ps_sd + ps_it + ps_pers + ps_duty

		# PS_CONF_2 (all uint8)
		ps_int = (_set.ps_conf_2.ps_int << VCNL4035_PS_CONF_2.PS_INT_START)
		ps_ns = (_set.ps_conf_2.ps_ns << VCNL4035_PS_CONF_2.PS_NS)
		ps_hd = (_set.ps_conf_2.ps_hd << VCNL4035_PS_CONF_2.PS_HD)
		ps_gain = (_set.ps_conf_2.ps_gain << VCNL4035_PS_CONF_2.PS_GAIN_START)
		gesture_mode = (_set.ps_conf_2.gesture_mode << VCNL4035_PS_CONF_2.GESTURE_MODE)
		gesture_int_en = (_set.ps_conf_2.gesture_int_en << VCNL4035_PS_CONF_2.GESTURE_INT_EN)
		ps_conf_2 = ps_int + ps_ns + ps_hd + ps_gain + gesture_mode + gesture_int_en

		# PS_CONF_3 (all uint8)
		ps_sc_en = _set.ps_conf_3.ps_sc_en << VCNL4035_PS_CONF_3.PS_SC_EN
		ps_ms_command = _set.ps_conf_3.ps_ms << VCNL4035_PS_CONF_3.PS_MS
		ps_trig = _set.ps_conf_3.ps_trig << VCNL4035_PS_CONF_3.PS_TRIG
		ps_af = _set.ps_conf_3.ps_af << VCNL4035_PS_CONF_3.PS_AF
		ps_smart_pers = _set.ps_conf_3.ps_smart_pers << VCNL4035_PS_CONF_3.PS_SMART_PERS
		ired_select = _set.ps_conf_3.ired_select << VCNL4035_PS_CONF_3.IRED_SELECT_START
		led_i_low = _set.ps_conf_3.led_i_low << VCNL4035_PS_CONF_3.LED_I_LOW
		ps_conf_3 = ps_sc_en + ps_ms_command + ps_trig + ps_af + ps_smart_pers + ired_select + led_i_low

		# PS_MS (all uint8)
		led_i = _set.ps_ms.led_i << VCNL4035_PS_MS.LED_I_START
		ps_spo = _set.ps_ms.ps_spo << VCNL4035_PS_MS.PS_SPO
		ps_sp = _set.ps_ms.ps_sp << VCNL4035_PS_MS.PS_SP
		ps_sc_cur = _set.ps_ms.ps_sc_cur << VCNL4035_PS_MS.PS_SC_CUR_START
		ps_ms = led_i + ps_spo + ps_sp + ps_sc_cur

		# PS_THDL (all uint8)
		ps_thdl_l = _set.ps_thdl & 0xff
		ps_thdl_m = _set.ps_thdl >> 8

		# PS_THDH (all uint8)
		ps_thdh_l = _set.ps_thdh & 0xff
		ps_thdh_m = _set.ps_thdh >> 8

		self.write_reg(PS_THDL_L_M, ps_thdl_l, ps_thdl_m)
		self.write_reg(PS_THDH_L_M, ps_thdh_l, ps_thdh_m)
		self.write_reg(PS_CONF_1_2, ps_conf_1, ps_conf_2)
		self.write_reg(PS_CONF_3_MS, ps_conf_3, ps_ms)

	# High level read functions
	def read_data(self):
		# Read the Proximity Sensor data (3x uint16)
		self.i2c.readfrom_into( self.addr, self.buf6 )
		return struct.unpack( "<HHH", self.buf6 )

	# Make the functions bellow in the .cpp file
	# uint16_t readPS1Data();
	# uint16_t readPS2Data();
	# uint16_t readPS3Data();

	@property
	def version(self):
		# return uint16_t
		return self.read_reg( VISHAY_VERSION_REG )

	def read_int_flags(self):
		""" Read interrupt flags and clear them (unit8, see INT_Flag in datasheet) """
		# bit 7: GESTURE_DATA_READY_FLAG
		# bit 6: PS3_SPFLAG, PS entering protection mode
		# bit 5: ALS_IF_L, ALS crossing low THD INT trigger event
		# bit 4: ALS_IF_H, ALS crossing high THD INT trigger event
		# bit 3: PS2_SPFLAG, PS entering protection mode
		# bit 2: PS1_SPFLAG, PS entering protection mode
		# bit 1: PS_IF_CLOSE, PS rises above PS_THDH INT trigger event
		# bit 0: PS_IF_AWAY, PS drops below PS_THDL INT trigger event
		return self.read_reg( RES_INT_FLAGS )>>8

	# High level write functions
	def set_ps_integration_time(self, int_time): 
		""" :param int_time: see VCNL4035_PS_IT constants """
		self.write_reg_bits( PS_CONF_1_2, L_BYTE, VCNL4035_PS_CONF_1.PS_IT_START, VCNL4035_PS_CONF_1.PS_IT_END, int_time )

	def set_led_current(self, led_current):
		""" :param led_current: one of the VCNL4035_LED_I constants """
		self.write_reg_bits( PS_CONF_3_MS, H_BYTE, VCNL4035_PS_MS.LED_I_START, VCNL4035_PS_MS.LED_I_END, led_current )

	def set_ps_trigger(self):
		""" Activate Gesture Trigger interruption """
		self.write_reg_bits( PS_CONF_3_MS, L_BYTE, 2, 2, 1 )

	def clearPsCloseFlag(self):
		raise NotImplementedError()

	def prox_int_thres_low(self, val):
		""" Set Proximity Sensor Interrupt Thresold (low value)
		    :param val: uint16_t value """
		self.write_reg( PS_THDL_L_M, val & 0xFF, val >> 8 ) # lowByte, HighByte

	def prox_int_thres_high(self, val):
		""" Set Proximity Sensor Interrupt Thresold (high value)
		    :param val: uint16_t value """
		self.write_reg( PS_THDH_L_M, val & 0xFF, val >> 8 ) # LowByte, HighByte

	# Make the functions bellow in the .cpp file
	# void setPsDutyCycle(VCNL4035_PS_DUTY duty_cycle);
	# void setPsShutdown(VCNL4035_PS_SD shutdown);
	# void setPsDataResolution(VCNL4035_PS_HD resolution);
	# void setPsActiveForce(VCNL4035_PS_AF on_off);
	# void setPsIredSelect(VCNL4035_IRED_SELECT ired);

	# Hardware Specfic Functions (VCNL4035_Lib_Hardware.cpp)
	# Raw I2C reads and writes
	# DOMEU: Lets see if we can avoids this!
	#
	#bool i2cWriteRegBits(uint8_t reg, uint8_t msb_lsb, uint8_t start_bit, uint8_t end_bit, uint8_t val);
	#bool i2cWriteReg(uint8_t reg, uint8_t low_byte, uint8_t high_byte);
	#bool i2cWriteByte(uint8_t val);
	#bool i2cReadReg(uint8_t reg, uint16_t &val);
	#bool i2cReadPsData(uint16_t *val);

	# Hardware Specfic Functions (VCNL4035_Lib_Hardware.cpp) 

	def read_int( self ):
		""" Read interrupt Pin """
		return self.int_pin.value()

	def set_int_pin( self, int_pin ): # uint8
		""" Setup the IRQ pin and callback """
		global irq_check, irq_count
		self.int_pin = int_pin
		self.int_pin.irq( handler=irq_cb, trigger=Pin.IRQ_FALLING )
		irq_check=irq_count

	def wait_data( self, timeout_ms=None ):
		""" Wait IRQ then read & returns the data. May return None in case of TimeOut! """
		global irq_check, irq_count
		irq_check = irq_count 
		self.read_int_flags() # reset potential last IRQ 
		_start = time.ticks_ms()
		while irq_count <= irq_check:
			time.sleep_ms( 1 ) # minimal period is 3 ms
			if (timeout_ms!=None) and (time.ticks_diff( time.ticks_ms(), _start )>timeout_ms ):				
				return None
		return self.read_data()

