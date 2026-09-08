""" vcnldefs.py - VCNL3045 definition for Vishay VCNL4035 Proximity sensor for MicroPython  

* Source   :  https://github.com/mchobby/esp8266-upy/vcnl4035
* Author(s):  Meurisse D. from MCHobby (shop.mchobby.be). 
"""
from micropython import const


# Acceptable VCNL4035 version 
VISHAY_VERSION_LSB = const( 0x80 )
VISHAY_VERSION_MSB = const( 0x00 )

# VCNL4035 I2C register addresses 
ALS_CONF_1_2= const( 0x00 )
ALS_THDH_1_2= const( 0x01 )
ALS_THDL_1_2= const( 0x02 )
PS_CONF_1_2 = const( 0x03 )
PS_CONF_3_MS= const( 0x04 )
PS_CANC_L_M = const( 0x05 )
PS_THDL_L_M = const( 0x06 )
PS_THDH_L_M = const( 0x07 )
PS1_DATA_REG = const( 0x08 )
PS2_DATA_REG = const( 0x09 )
PS3_DATA_REG = const( 0x0A )
ALS_DATA_L_M = const( 0x0B )
WHITE_DATA_L_M = const( 0x0C )
RES_INT_FLAGS = const( 0x0D )
VISHAY_VERSION_REG = const( 0x0E )

H_BYTE = const( 1 )
L_BYTE = const( 0 )

# VCNL4035 Operational Modes 
class VCNL4035_MODES:
	GESTURE = const(0)
	PROXIMITY = const(1)
	AMBIENT_LIGHT = const(2)

# VCNL4035 Register Bit Locations 
class VCNL4035_PS_CONF_1:
	PS_SD = const( 0 )
	PS_IT_START = const( 1 )
	PS_IT_END = const( 3 )
	PS_PRES_START = const( 4 )
	PS_PRES_END = const( 5 )
	PS_DUTY_START = const( 6 )
	PS_DUTY_END = const( 7 )

class VCNL4035_PS_CONF_2:
	PS_INT_START = const( 0 )
	PS_INT_END = const( 1 )
	PS_NS = const( 2 )
	PS_HD = const( 3 )
	PS_GAIN_START = const( 4 )
	PS_GAIN_END = const( 5 )
	GESTURE_MODE = const( 6 )
	GESTURE_INT_EN = const( 7 )

class VCNL4035_PS_CONF_3:
	PS_SC_EN = const( 0 )
	PS_MS = const( 1 )
	PS_TRIG = const( 2 )
	PS_AF = const( 3 )
	PS_SMART_PERS = const( 4 )
	IRED_SELECT_START = const( 5 )
	IRED_SELECT_END = const( 6 )
	LED_I_LOW = const( 7 )

class VCNL4035_PS_MS:
	LED_I_START = const( 0 )
	LED_I_END = const( 2 )
	PS_SPO = const( 3 )
	PS_SP = const( 4 )
	PS_SC_CUR_START = const( 5 )
	PS_SC_CUR_END = const( 6 )
	RESERVED = const( 7 )

class VCNL4035_INT_FLAG:
	PS_IF_AWAY = const( 0 )
	PS_IF_CLOSE = const( 1 )
	PS1_SPFLAG = const( 2 )
	PS2_SPFLAG = const( 3 )
	ALS_IF_H = const( 4 )
	ALS_IF_L = const( 5 )
	PS3_SPFLAG = const( 6 )
	GESTURE_DATA_READY_FLAG = const( 7 )

# VCNL Command Parrameters 

# PS CONF 1 

# Proximity Sensor Power Shutdown 
class VCNL4035_PS_SD:
	PS_SD_POWER_ON = const(0) # Turns on proximity sensor
	PS_SD_POWER_SHUTDOWN = const(1) # Shutdown proximity sensor

# Proximity Sensor Integration (T = 50 micro sec)
class VCNL4035_PS_IT:
	PS_IT_50us  = const(0) # 1.0 T
	PS_IT_75us  = const(1) # 1.5 T
	PS_IT_100us = const(2) # 2.0 T
	PS_IT_125us = const(3) # 2.5 T
	PS_IT_150us = const(4) # 3.0 T
	PS_IT_175us = const(5) # 3.5 T
	PS_IT_200us = const(6) # 4.0 T
	PS_IT_400us = const(7) # 8.0 T

# Proximity Sensor Interrupt Persistance *
class VCNL4035_PS_PERS:
	PS_PERS_1_READING = const(0)
	PS_PERS_2_READING = const(1)
	PS_PERS_3_READING = const(2)
	PS_PERS_4_READING = const(3)


# Proximity Sensor Duty Cycle
class VCNL4035_PS_DUTY:
	PS_DUTY_1_40 = const(0)  # 40 off pulses for every 1 on pulse
	PS_DUTY_1_80 = const(1)  # 80 off pulses for every 1 on pulse
	PS_DUTY_1_160 = const(2) # 160 off pulses for every 1 on pulse
	PS_DUTY_1_320 = const(3) # 320 off pulses for every 1 on pulse


# PS CONF 2

# Proximity Sensor Interrupt Trigger Mode
class VCNL4035_PS_INT:
	PS_INT_DISABLE = const(0)
	PS_INT_CLOSING = const(1)
	PS_INT_AWAY = const(2)
	PS_INT_CLOSING_AWAY = const(3)

# Proximity Sensor Sensitivity
class VCNL4035_PS_NS:
	PS_NS_TWO_STEP_MODE_TIMES_4 = const(0)
	PS_NS_TWO_STEP_MODE_TIMES_1 = const(1)

# Proximity Sensor Data Resolution
class VCNL4035_PS_HD:
	PS_HD_12_BIT = const(0) # 12 bit resolution
	PS_HD_16_BIT = const(1) # 16 bit resolution


# Proximity Sensor Gain Modes
class VCNL4035_PS_GAIN:
	PS_GAIN_TWO_STEP_MODE = const(0)
	PS_GAIN_SINGLE_MODE_8 = const(2)
	PS_GAIN_SINGLE_MODE_1 = const(3)

# Proximity Sensor Gesture Mode
class VCNL4035_GESTURE_MODE:
	GESTURE_MODE_DISABLE = const(0)
	GESTURE_MODE_ENABLE = const(1)

# Proximity Sensor Gesture Mode Interrupt Enable
class VCNL4035_GESTURE_INT_EN:
	GESTURE_INT_EN_DISABLE = const(0)
	GESTURE_INT_EN_ENABLE = const(1)

# PS CONF 3

# Proximity Sensor Sunlight Cancel Enable
class VCNL4035_PS_SC_EN:
	PS_SC_EN_OFF = const(0)
	PS_SC_EN_ON = const(1)


# Proximity Sensor Interrupt Pin Functionally
class VCNL4035_PS_MS_COMMAND:
	PS_MS_NORMAL_MODE = const(0)
	PS_MS_LOGIC_MODE = const(1)

# Proximity Sensor Active Force Mode Trigger
class VCNL4035_PS_TRIG:
	PS_TRIG_LOW = const(0)
	PS_TRIG_HIGH = const(1)

# Proximity Sensor Active Force Mode Enable
class VCNL4035_PS_AF:
	PS_AF_OFF = const(0)
	PS_AF_ON = const(1)

# Proximity Sensor Smart Persistance Mode Enable
class VCNL4035_PS_SMART_PERS:
	PS_SMART_PERS_OFF = const(0)
	PS_SMART_PERS_ON = const(1)

# Proximity Sensor IRED Selection
class VCNL4035_IRED_SELECT:
	IRED_SELECT_1 = const(0)
	IRED_SELECT_2 = const(1)
	IRED_SELECT_3 = const(2)

# Proximity Sensor Smart LED Low Current Mode:
# Reduces the LED current [Amps] by a factor of 10.
class VCNL4035_LED_I_LOW:
	LED_I_LOW_OFF = const(0)
	LED_I_LOW_ON = const(1)

# PS MS

# Proximity Sensor LED Current
class VCNL4035_LED_I:
	LED_I_50mA = const(0)
	LED_I_75mA = const(1)
	LED_I_100mA = const(2)
	LED_I_120mA = const(3)
	LED_I_140mA = const(4)
	LED_I_160mA = const(5)
	LED_I_180mA = const(6)
	LED_I_200mA = const(7)

# Proximity Sensor Sunlight Protect Output
class VCNL4035_PS_SPO:
	PS_SPO_00H = const(0)
	PS_SPO_FFH = const(1)

# Proximity Sensor Sunlight Protect Capability
class VCNL4035_PS_SP:
	PS_SP_TYPICAL_1 = const(0)   # Typical sunlight capability
	PS_SP_TYPICAL_1_5 = const(1) # 1.5 x Typical sunlight capability

# Proximity Sensor Sunlight Cancel Current
class VCNL4035_PS_SC_CUR:
	PS_SC_CUR_TYPICAL_TIMES_1 = const(0)
	PS_SC_CUR_TYPICAL_TIMES_2 = const(1)
	PS_SC_CUR_TYPICAL_TIMES_4 = const(2)
	PS_SC_CUR_TYPICAL_TIMES_8 = const(3)

# Structure Defintions
class ps_conf_1_t:
	def __init__( self ):
		self.ps_sd = VCNL4035_PS_SD.PS_SD_POWER_ON
		self.ps_it = VCNL4035_PS_IT.PS_IT_50us
		self.ps_pers = VCNL4035_PS_PERS.PS_PERS_1_READING
		self.ps_duty = VCNL4035_PS_DUTY.PS_DUTY_1_40

class ps_conf_2_t:
	def __init__( self ):
		self.ps_int = VCNL4035_PS_INT.PS_INT_DISABLE
		self.ps_ns = VCNL4035_PS_NS.PS_NS_TWO_STEP_MODE_TIMES_4
		self.ps_hd = VCNL4035_PS_HD.PS_HD_12_BIT
		self.ps_gain = VCNL4035_PS_GAIN.PS_GAIN_TWO_STEP_MODE
		self.gesture_mode = VCNL4035_GESTURE_MODE.GESTURE_MODE_DISABLE
		self.gesture_int_en = VCNL4035_GESTURE_INT_EN.GESTURE_INT_EN_DISABLE


class ps_conf_3_t:
	def __init__( self ):
		self.ps_sc_en = VCNL4035_PS_SC_EN.PS_SC_EN_OFF
		self.ps_ms = VCNL4035_PS_MS_COMMAND.PS_MS_NORMAL_MODE
		self.ps_trig = VCNL4035_PS_TRIG.PS_TRIG_LOW
		self.ps_af = VCNL4035_PS_AF.PS_AF_OFF
		self.ps_smart_pers = VCNL4035_PS_SMART_PERS.PS_SMART_PERS_OFF
		self.ired_select = VCNL4035_IRED_SELECT.IRED_SELECT_1
		self.led_i_low = VCNL4035_LED_I_LOW.LED_I_LOW_OFF

class ps_ms_t:
	def __init__( self ):
		self.led_i = VCNL4035_LED_I.LED_I_50mA
		self.ps_spo = VCNL4035_PS_SPO.PS_SPO_00H
		self.ps_sp = VCNL4035_PS_SP.PS_SP_TYPICAL_1
		self.ps_sc_cur = VCNL4035_PS_SC_CUR.PS_SC_CUR_TYPICAL_TIMES_1

class ps_settings_t:
	def __init__( self ):
		self.ps_thdl = 0 # uint16
		self.ps_thdh = 0 # uint16 
		self.ps_conf_1 = ps_conf_1_t()
		self.ps_conf_2 = ps_conf_2_t()
		self.ps_conf_3 = ps_conf_3_t()
		self.ps_ms = ps_ms_t()
