# Grove6dip - MicroPython library to support "Grove 6 DIP Switch" from
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

from grove5way import GroveMultiSwitch, ButtonEvent, VID_MULTI_SWITCH

__version__ = "0.0.1"

class SixDipEvent( ButtonEvent ):
	def __init__( self, switch_count ):
		super().__init__( switch_count )

	def dip( self, dip_nr ):
		assert 1<=dip_nr<=switch_count, "Invalid DIP number"
		return self._button[dip_nr-1] == 0

	def dip_events( self, dip_nr ):
		# Return initialized DecodedEvent object
		assert 1<=dip_nr<=switch_count, "Invalid DIP number"
		return self.decode_button_events( dip_nr-1 )

class Grove6Dip(GroveMultiSwitch):
	def __init__(self, i2c, address=0x03 ):
		super().__init__( i2c, address, SixDipEvent )
		self.probe_vendor_id( VID_MULTI_SWITCH ) # Check device vendor ID
		self.device_version() # Initialize device version
