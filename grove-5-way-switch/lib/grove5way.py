# Grove5Way - MicroPython library to support "Grove 5 Way Switch" from
#      SeeedStudio.
#
# Copyright (c) 2021 Meurisse D. for MCHobby.be - portage to MicroPython.
# Copyright (c) 2018- Seeed Technology Co., Ltd. - Arduino Library
#
# Keeping the original license:
# 	This code is release as The MIT License (MIT) as the original
# 	arduino library.
#
# Based on https://github.com/Seeed-Studio/Grove_Multi_Switch
#
from micropython import const
import time, struct

__version__ = "0.0.1"

CMD_GET_DEV_ID		= const( 0x00 ) # gets device ID information
CMD_GET_DEV_EVENT	= const( 0x01 ) # gets device event status
CMD_EVENT_DET_MODE	= const( 0x02 )	# enable button EVENT detect mode (Simple/double click, long press)
CMD_BLOCK_DET_MODE	= const( 0x03 )	# enable button BLOCK detect mode (read entry state)
CMD_AUTO_SLEEP_ON	= const( 0xb2 )	# enable device auto sleep mode
CMD_AUTO_SLEEP_OFF	= const( 0xb3 )	# disable device auto sleep mode (default mode)
CMD_SET_ADDR		= const( 0xc0 )	# sets device i2c address
CMD_RST_ADDR		= const( 0xc1 )	# resets device i2c address
CMD_TEST_TX_RX_ON	= const( 0xe0 )	# enable TX RX pin test mode
CMD_TEST_TX_RX_OFF	= const( 0xe1 )	# disable TX RX pin test mode
CMD_TEST_GET_VER	= const( 0xe2 )	# use to get software version
CMD_GET_DEVICE_UID	= const( 0xf1 )	# use to get chip id

VID_MULTI_SWITCH = const( 0x2886 ) # Vendor ID (SeeedStudio)

PID_5_WAY_TACTILE_SWITCH = const( 0x0002 ) # Grove 5-Way Tactile
PID_6_POS_DIP_SWITCH	 = const( 0x0003 ) # Grove 6-Position DIP Switch

# --- Event status ---
RAW_DIGITAL_BTN_PRESSED = const( 0 )
RAW_DIP_SWITCH_ON		= const( 0 )

BTN_EV_NO_EVENT     = const( 0x0 )
BTN_EV_HAS_EVENT    = const( 0x80000000 )
BTN_EV_RAW_STATUS   = const( 1 << 0 )
BTN_EV_SINGLE_CLICK = const( 1 << 1 )
BTN_EV_DOUBLE_CLICK = const( 1 << 2 )
BTN_EV_LONG_PRESS   = const( 1 << 3 )
BTN_EV_LEVEL_CHANGED= const( 1 << 4 )

class GroveMultiSwitchError( Exception ):
	pass

class DecodedEvents:
	# Class to keep an easy access to Event bits
	def __init__( self ):
		self._single_click = False
		self._double_click = False
		self._long_press   = False
		self._level_changed= False

	def decode( self, value ):
		# Decode the byte value to the events
		self._single_click = ( value & BTN_EV_SINGLE_CLICK) == BTN_EV_SINGLE_CLICK
		self._double_click = ( value & BTN_EV_DOUBLE_CLICK) == BTN_EV_DOUBLE_CLICK
		self._long_press   = ( value & BTN_EV_LONG_PRESS) == BTN_EV_LONG_PRESS
		self._level_changed= ( value & BTN_EV_LEVEL_CHANGED) == BTN_EV_LEVEL_CHANGED # Used for DIP Switch

	@property
	def has_event( self ):
		return self._single_click or self._double_click or self._long_press or self._level_changed

	@property
	def single_click( self ):
		return self._single_click

	@property
	def double_click( self ):
		return self._double_click

	@property
	def long_press( self ):
		return self._long_press

	@property
	def level_changed( self ):
		return self._level_changed


class ButtonEvent:
	def __init__(self, switch_count ):
		# Structure returned
		self._event = 0 # uInt32 : BTN_EV_NO_EVENT/BTN_EV_HAS_EVENT
		self._button = list( None for i in range(switch_count) ) # Bytes

		self._events = DecodedEvents()

	def readfrom_buf( self, buf ):
		# Initialize internal structure from buffer readed from device
		self._event = struct.unpack('<I', buf[0:4] )[0] # 4 first bytes is a uInt32
		for i in range(len(self._button)):
			self._button[i] = buf[4+i]

	def copy( self, _from ):
		# Copy the data from another ButtonEvent
		self._event = _from._event
		for i in range( len( self._button )):
			self._button[i] = _from._button[i]

	def decode_button_events(self, index ):
		# Interpret the event stored inside the _button[i] and return a
		# properly initialized DecodedEvents() instance
		self._events.decode( self._button[index] ) # decode value returned by MCU
		return self._events

	@property
	def has_event( self ):
		return ( self._event & BTN_EV_HAS_EVENT) ==  BTN_EV_HAS_EVENT


class FiveWayEvent( ButtonEvent ):
	def __init__( self, switch_count ):
		super().__init__( switch_count )

	@property
	def a( self ):
		return self._button[0] == 0

	@property
	def b( self ):
		return self._button[1] == 0

	@property
	def c( self ):
		return self._button[2] == 0

	@property
	def d( self ):
		return self._button[3] == 0

	@property
	def e( self ):
		return self._button[4] == 0

	@property
	def up( self ):
		return self._button[1] == 0

	@property
	def up_events( self ):
		# Return initialized DecodedEvent object
		return self.decode_button_events( 1 )

	@property
	def down( self ):
		return self._button[3] == 0

	@property
	def down_events( self ):
		# Return initialized DecodedEvent object
		return self.decode_button_events( 3 )

	@property
	def left( self ):
		return self._button[2] == 0

	@property
	def left_events( self ):
		# Return initialized DecodedEvent object
		return self.decode_button_events( 2 )

	@property
	def right( self ):
		return self._button[0] == 0

	@property
	def right_events( self ):
		# Return initialized DecodedEvent object
		return self.decode_button_events( 0 )

	@property
	def click( self ):
		return self._button[4] == 0

	@property
	def click_events( self ):
		# Return initialized DecodedEvent object
		return self.decode_button_events( 4 )


class GroveMultiSwitch:
	def __init__(self, i2c, address=0x00, EventClass=ButtonEvent ):
		# use a descendant of ButtonEvent as EventClass
		self.i2c = i2c
		self.address = address
		self.buf1 = bytearray(1)
		self.buf4 = bytearray(4)
		self.lock = True # security lock avoiding to change address
		self.versions = bytearray( 10 ) # _MULTI_SWITCH_VERSIONS_SZ
		self.version = None
		self._switch_count = None # will be read & buffered @ first read
		self._EventClass  = EventClass # Class used to create _button_event; descendant of ButtonEvent
		self._event_buf    = None # Buffer used to grab event data; initialized @ first get_event()
		self._button_event = None # ButtonEvent class; Will be initialized at get_event()
		self._last_event   = None # last button event
		self._event_initial= False# Just know when event is initialized

	def read_dev( self, data ):
		self.i2c.readfrom_into( self.address, data )

	def write_dev( self, data ):
		self.i2c.writeto( self.address, data )

	def read_reg( self, reg, data ):
		self.buf1[0] = reg
		self.write_dev( self.buf1 )
		time.sleep_ms( 1 ) # required
		self.read_dev( data )

	def probe_vendor_id( self, id ):
		# Read the device and check vendor ID. Will raise exception
		# ID is a uint32
		self.read_reg( CMD_GET_DEV_ID, self.buf4 )
		_read_id = struct.unpack('<I', self.buf4 )[0] # Uint32
		# Vendor ID = 16 first bits
		if (_read_id >> 16) != id:
			raise GroveMultiSwitchError( 'Invalid vendor ID 0x%x . Wrong device!' % (_read_id >> 16)  )
		return _read_id >> 16

	def device_version( self ):
		# Get device versions bytes & initialize the version value
		self.read_reg( CMD_TEST_GET_VER, self.versions )
		self.version = (self.versions[6]-48) * 10 + (self.versions[8]-48)
		return self.version

	def unlock( self ):
		self.lock = False


	def change_address( self, new_address ):
		if self.lock:
			raise GroveMultiSwitchError( 'Call to unlock() required before updating module address!' )
		data = bytearray( 2 )
		data[0] = CMD_SET_ADDR
		data[1] = new_address

		self.write_dev( data )

	@property
	def switch_count( self ):
		# return the number of switches registered in the board
		if self._switch_count != None:
			return self._switch_count

		self.read_reg( CMD_GET_DEV_ID, self.buf4 )
		_read_id = struct.unpack('<I', self.buf4 )[0] # Uint32
		# Product ID = 16 last bits
		_pid = _read_id & 0xFFFF
		if _pid == PID_5_WAY_TACTILE_SWITCH:
			self._switch_count = 5
		elif _pid == PID_6_POS_DIP_SWITCH:
			self._switch_count = 6
		else:
			self._switch_count = 0
		return self._switch_count

	def set_event_mode( self, enabled ):
		""" activate event detection mode. Events like change, single/double click, long press.
		    Note: Current status can be read immediately with get_event()

			--- Event ENABLED ---
			5 Way Switch events: single/double click, long press
			DIP Switch events  : level changed
			--- Event DISABLED ---
			5 Way Switch status: press/non-press
			DIP Switch status  : switch on/off
			"""
		self.buf1[0] = CMD_EVENT_DET_MODE if enabled else CMD_BLOCK_DET_MODE
		self.write_dev( self.buf1 )

	def get_event( self ):
		""" Get button/switch event. See the set_event_mode() for details.

			Returns a ButtonEvent instance. """
		# NULL if error, such as device unexist.
		#   .event = BTN_EV_NO_EVENT if no event
		#   .event = BTN_EV_HAS_EVENT if event occured,
		#    and .button to check event of each button/switch.
		if self._event_buf == None:
			self._event_buf = bytearray( 4+self.switch_count )
			self._button_event = self._EventClass( self.switch_count )
			self._last_event   = self._EventClass( self.switch_count )

		self.read_reg( CMD_GET_DEV_EVENT, self._event_buf )
		self._button_event.readfrom_buf( self._event_buf )
		if self.version > 1:
			return self._button_event
		# Fix: v0.1 will miss event BTN_EV_LEVEL_CHANGED
		#      if this API called frequently.
		if not(self._event_initial):
			self._last_event.copy( self._button_event )
			self._event_initial = True

		for i in range( len(self._button_event._button) ):
			self._button_event._button[i] = self._button_event._button[i] & (0xFF ^ BTN_EV_LEVEL_CHANGED)
			if ((self._button_event._button[i] ^ self._last_event._button[i]) & BTN_EV_RAW_STATUS) == BTN_EV_RAW_STATUS:
				self._button_event._button[i] = self._button_event._button[i] | BTN_EV_LEVEL_CHANGED
				self._button_event._event = self._button_event._event | BTN_EV_HAS_EVENT
		self._last_event.copy( self._button_event )
		return self._button_event

class Grove5Way(GroveMultiSwitch):
	def __init__(self, i2c, address=0x03 ):
		super().__init__( i2c, address, FiveWayEvent )
		self.probe_vendor_id( VID_MULTI_SWITCH ) # Check device vendor ID
		self.device_version() # Initialize device version
