""" rfm69.py - SX1231 driver for RFM69 Packet Radio module (SPI interface)
               suitable for 433 MHz - 868 MHz - 915 MHz

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
RFM69HCW breakout : https://www.adafruit.com/product/3071

see project: https://github.com/mchobby/esp8266-upy/tree/master/rfm69
"""
#
# 2022 Feb 11, DMeurisse (MCHobby)
#    - Make it MicroPython plateform independant (refer to licenses here below)
#    - Based on https://github.com/arkorobotics/rfm69-micropython for Pyboard (see LICENSE file)
#    - Includes merging with https://github.com/adafruit/Adafruit_CircuitPython_RFM69 (MIT License)
#
# Prior Art:
#   Ported to Micropython by Arko at EMFCAMP 2016 - HABVILLE
#   rfm69-python : Copyright (C) 2016 Russ Garrett
#   ukhasnet-rfm69: Copyright (C) 2014 Phil Crump, James Coxon
#
#   Based on RF22 Copyright (C) 2011 Mike McCauley ported to mbed by Karl Zweimueller
#   Based on RFM69 LowPowerLabs (https://github.com/LowPowerLab/RFM69/)
#

from micropython import const
from time import sleep, sleep_us, sleep_ms, ticks_ms, ticks_diff
import random


__version__ = "0.0.1"
__repo__ = "https://github.com/mchobby/esp8266-upy/rfm69"

# The crystal oscillator frequency and frequency synthesizer step size.
# See the datasheet for details of this calculation.
_FXOSC = 32000000.0
_FSTEP = _FXOSC / 524288

# Register definition
RFM69_SPI_WRITE_MASK 		= const( 0x80 )
RFM69_MAX_MESSAGE_LEN 		= const( 64 )
RFM69_FIFO_SIZE 			= const( 64 )

RFM69_MODE_SLEEP 			= const( 0x00 )  # 0.1uA
RFM69_MODE_STDBY 			= const( 0x04 )  # 1.25mA
RFM69_MODE_RX 				= const( 0x10 )  # 16mA
RFM69_MODE_TX 				= const( 0x0c )  # >33mA

RFM69_REG_58_TEST_LNA 		= const( 0x58 )
RF_TESTLNA_SENSITIVE 		= const( 0x2D )
RFM69_REG_FIFO 				= const( 0x00 )
RFM69_REG_OPMODE 			= const( 0x01 )
RFM69_REG_DATA_MODUL 		= const( 0x02 )
RFM69_REG_BITRATE_MSB		= const( 0x03 )
RFM69_REG_BITRATE_LSB		= const( 0x04 )
RFM69_REG_FDEV_MSB 			= const( 0x05 )
RFM69_REG_FDEV_LSB 			= const( 0x06 )
RFM69_REG_FRF_MSB 			= const( 0x07 )
RFM69_REG_FRF_MID 			= const( 0x08 )
RFM69_REG_FRF_LSB 			= const( 0x09 )
RFM69_REG_AFC_CTRL			= const( 0x0B )
RFM69_REG_VERSION 			= const( 0x10 )  #Version and serial number
RFM69_REG_PA_LEVEL 			= const( 0x11 )
RFM69_REG_PA_RAMP 			= const( 0x12 )
RFM69_REG_OCP 				= const( 0x13 )
RFM69_REG_LNA 				= const( 0x18 )
RFM69_REG_RX_BW 			= const( 0x19 )
RFM69_REG_AFC_FEI 			= const( 0x1E )
RFM69_REG_AFC_BW 			= const( 0x1A )
RFM69_REG_RSSI_CONFIG		= const( 0x23 )
RFM69_REG_RSSI_VALUE 		= const( 0x24 )
RFM69_REG_DIO_MAPPING1 		= const( 0x25 )
RFM69_REG_DIO_MAPPING2 		= const( 0x26 )
RFM69_REG_IRQ_FLAGS1 		= const( 0x27 )
RFM69_REG_IRQ_FLAGS2 		= const( 0x28 )
RFM69_REG_PREAMBLE_MSB 		= const( 0x2C )
RFM69_REG_PREAMBLE_LSB 		= const( 0x2D )
RFM69_REG_SYNC_CONFIG		= const( 0x2E )
RFM69_REG_SYNC_VALUE1 		= const( 0x2F )
RFM69_REG_SYNC_VALUE2 		= const( 0x30 )
RFM69_REG_PACKET_CONFIG1 	= const( 0x37 )
RFM69_REG_PAYLOAD_LENGTH 	= const( 0x38 )
RFM69_REG_FIFO_THRESHOLD 	= const( 0x3C )
RFM69_REG_PACKET_CONFIG2 	= const( 0x3D )
RFM69_REG_AES_KEY1 			= const(0x3E)
RFM69_REG_TEST_DAGC			= const( 0x6F )
RF_OPMODE_SEQUENCER_ON		= const( 0x00 ) # Default
RF_OPMODE_LISTEN_OFF		= const( 0x00 ) # Default
RF_DATAMODUL_DATAMODE_PACKET= const( 0x00 ) # Default
RF_DATAMODUL_MODULATIONTYPE_FSK 	= const( 0x00 ) # Default
RF_DATAMODUL_MODULATIONSHAPING_00 	= const( 0x00 ) # Default
RF_AFCLOWBETA_OFF 			= const( 0x00 ) # Default
RF_PALEVEL_PA0_ON 			= const( 0x80 ) # Default
RF_PALEVEL_PA0_OFF 			= const( 0x00 )
RF_PALEVEL_PA1_ON 			= const( 0x40 )
RF_PALEVEL_PA1_OFF 			= const( 0x00 ) # Default
RF_PALEVEL_PA2_ON 			= const( 0x20 )
RF_PALEVEL_PA2_OFF 			= const( 0x00 ) # Default
RF_PARAMP_500 				= const( 0x03 )
RF_OCP_OFF 					= const( 0x0F )
RF_OCP_ON 					= const( 0x1A ) # Default
RF_OCP_TRIM_95 				= const( 0x0A )
RF_LNA_ZIN_50 				= const( 0x00 )
RF_RXBW_DCCFREQ_010 		= const( 0x40 ) # Default
RF_RXBW_MANT_16 			= const( 0x00 )
RF_RXBW_EXP_2 				= const( 0x02 )
RF_AFCFEI_AFCAUTOCLEAR_ON	= const( 0x08 )
RF_AFCFEI_AFCAUTO_ON 		= const( 0x04 )
RF_RSSI_DONE 				= const( 0x02 )
RF_RSSI_START 				= const( 0x01 )
RF_DIOMAPPING1_DIO0_01 		= const( 0x40 )
RF_DIOMAPPING2_CLKOUT_OFF	= const( 0x07 ) # Default
RF_IRQFLAGS1_TXREADY 		= const( 0x20 )
RF_IRQFLAGS2_PACKETSENT 	= const( 0x08 )
RF_IRQFLAGS2_PAYLOADREADY	= const( 0x04 )
RF_SYNC_ON					= const( 0x80 ) # Default
RF_SYNC_FIFOFILL_AUTO 		= const( 0x00 ) # Default -- when sync interrupt occurs
RF_SYNC_SIZE_2 				= const( 0x08 )
RF_SYNC_SIZE_4 				= const( 0x18 )
RF_SYNC_TOL_0 				= const( 0x00 ) # Default
RF_PACKET1_FORMAT_VARIABLE	= const( 0x80 )
RF_PACKET1_DCFREE_OFF 		= const( 0x00 ) # Default
RF_PACKET1_CRC_ON 			= const( 0x10 ) # Default
RF_PACKET1_CRCAUTOCLEAR_ON	= const( 0x00 ) # Default
RF_PACKET1_ADRSFILTERING_OFF= const( 0x00 ) # Default
RF_FIFOTHRESH_TXSTART_FIFOTHRESH = const( 0x00 )
RF_FIFOTHRESH_TXSTART_FIFONOTEMPTY = const( 0x80 ) # Default
RF_FIFOTHRESH_VALUE 			 = const( 0x0F ) # Default
RF_PACKET2_RXRESTARTDELAY_2BITS  = const( 0x10 )
RF_PACKET2_AUTORXRESTART_ON 	 = const( 0x02 ) # Default
RF_PACKET2_AES_OFF				 = const( 0x00 ) # Default
RF_TEMP1_MEAS_RUNNING			 = const( 0x04 )
RF_DAGC_IMPROVED_LOWBETA0		 = const( 0x30 )# Recommended default
RFM69_REG_TEMP1				 	 = const( 0x4E )
RFM69_REG_TEMP2				 	 = const( 0x4F )
RF_TEMP1_MEAS_START				 = const( 0x08 )
RFM69_REG_TEST_PA1			 	 = const( 0x5A )
RFM69_REG_TEST_PA2			 	 = const( 0x5C )
RF_RXBW_EXP_5					 = const( 0x05 )
RF_RXBW_MANT_24					 = const( 0x10 )
RF_PARAMP_40					 = const( 0x09 )
RF_AFCFEI_AFCAUTO_OFF			 = const( 0x00 )
RF_AFCFEI_AFCAUTOCLEAR_OFF		 = const( 0x00 )
#RF_SYNC_SIZE_4					 = const( 0x18 )
#RF_RSSITHRESH_VALUE				 = const( 0xE4 )
RF_TEST_PA1_BOOST = const(0x5D)
RF_TEST_PA2_BOOST = const(0x7C)
RF_TEST_PA1_NORMAL= const(0x55)
RF_TEST_PA2_NORMAL= const(0x70)

# RADIOHEAD SPECIFIC COMPATIBILITY CONSTANTS.
# (RadioHead appends 4 bytes to the transmitted data (at the head)
_RH_BROADCAST_ADDRESS = const(0xFF)
# The acknowledgement bit in the FLAGS
# The top 4 bits of the flags are reserved for RadioHead. The lower 4 bits are reserved for application layer use.
_RH_FLAGS_ACK = const(0x80)
_RH_FLAGS_RETRY = const(0x40)


def check_timeout(flag, limit):
	"""test for timeout waiting for specified flag"""
	timed_out = False
	start = ticks_ms()
	while not timed_out and not flag():
		if ticks_diff( ticks_ms(), start ) >= limit * 1000:
			timed_out = True
	return timed_out

class RFM69:
	def __init__(self, spi=None, nss=None, reset=None): # dio0_pin=None
		self.reset_pin = reset
		self.nss = nss # Pin('X5', Pin.OUT_PP)
		self.spi = spi
		self._mode = None
		self._tx_power = None
		self.high_power = True # RFM69HCW can accept higher value for tx_power

		# initialize timeouts and delays delays
		self.ack_wait        = 0.5 # The delay time before attempting a retry after not receiving an ACK
		self.receive_timeout = 0.5 # The amount of time to poll for a received packet. If no packet is received, the returned packet will be None
		self.xmit_timeout    = 2.0 # The amount of time to wait for the HW to transmit the packet. This is mainly used to prevent a hang due to a HW issue
		self.ack_retries     = 5   # The number of ACK retries before reporting a failure.
		self.ack_delay 		 = None# The delay time before attemting to send an ACK. If ACKs are being missed try setting this to .1 or .2.

		# ----------------------------------------------------------------------
		# initialize sequence number counter for reliabe datagram mode
		# and Fourth byte of the RadioHead header.
		# ----------------------------------------------------------------------
		self.sequence_number = 0
		self.seen_ids = bytearray(256) # create seen Ids list
		# initialize packet header
		# node address - default is broadcast (First byte of the RadioHead header)
		#    The default address of this Node. (0-255).
		#    If not 255 (0xff) then only packets address to this node will be accepted.
		#
		self.node = _RH_BROADCAST_ADDRESS
		# destination address - default is broadcast (Second byte of the RadioHead header)
		#    The default destination address for packet transmissions. (0-255).
		#    If 255 (0xff) then any receiving node should accept the packet.
		self.destination = _RH_BROADCAST_ADDRESS
		# ID - contains seq count for reliable datagram mode - Third byte of the RadioHead header.
		#    Automatically set to the sequence number when send_with_ack() used.
		self.identifier = 0
		# flags - identifies ack/reetry packet for reliable datagram mode
		#  - Upper 4 bits reserved for use by Reliable Datagram Mode.
		#  - Lower 4 bits may be used to pass information.
		self.flags = 0

		self.reset()
		self.tx_power = 13  # 13 dBm = 20mW (default value, safer for all modules)
		self.__idle()
		# Setup the chip in a similar way to the RadioHead RFM69 library.
		# Set FIFO TX condition to not empty and the default FIFO threshold to 15.
		self.spi_write(RFM69_REG_FIFO_THRESHOLD, 0b10001111)
		# Configure low beta off.
		self.spi_write(RFM69_REG_TEST_DAGC, 0x30)
		# Disable boost.
		self.spi_write( RFM69_REG_TEST_PA1, RF_TEST_PA1_NORMAL)
		self.spi_write( RFM69_REG_TEST_PA2, RF_TEST_PA2_NORMAL)

		self.sync_word = b"\x2D\xD4" # default rfm69
		self.preamble_length = 4 # Match the RadioHead preamble
		self.set_mode( RFM69_MODE_RX )
		self.last_rssi = self.rssi

		# Configure modulation for RadioHead library GFSK_Rb250Fd250 mode
		# by default.  Users with advanced knowledge can manually reconfigure
		# for any other mode (consulting the datasheet is absolutely
		# necessary!).
		self.modulation_shaping = 0b01  # Gaussian filter, BT=1.0
		self.bitrate = 250000  # 250kbs
		self.frequency_deviation = 250000  # 250khz
		self.rx_bw_dcc_freq = 0b111  # RxBw register = 0xE0
		self.rx_bw_mantissa = 0b00
		self.rx_bw_exponent = 0b000
		self.afc_bw_dcc_freq = 0b111  # AfcBw register = 0xE0
		self.afc_bw_mantissa = 0b00
		self.afc_bw_exponent = 0b000
		self.packet_format = 1  # Variable length.
		self.dc_free = 0b10  # Whitening

	@property
	def version(self):
		return self.spi_read( RFM69_REG_VERSION )

	def set_mode(self, newMode ):
		self.spi_write( RFM69_REG_OPMODE, (self.spi_read( RFM69_REG_OPMODE ) & 0xE3) | newMode)
		# Wait for the mode change by pulling the interrupt bit
		start = ticks_ms()
		while not self.spi_read( RFM69_REG_IRQ_FLAGS1 ) & 0b10000000:
			if ticks_diff( ticks_ms(), start ) >= 1000:
				raise RuntimeError( 'Change mode timeout!' )
		self._mode = newMode
		return newMode

	@property
	def mode(self):
		return self._mode

	def reset(self):
		""" Reset the module, then check it's working. """
		self.nss.high()
		# self.reset_pin = Pin('X4', Pin.OUT_PP)
		self.reset_pin.low()
		sleep_us(100)
		self.reset_pin.high()
		sleep_us(100)
		self.reset_pin.low()
		sleep_ms(5)


	def send( self, data, keep_listening=False, destination=None, node=None,
			  identifier=None, flags=None  ):
		""" Send a string of data using the transmitter. Can only send 60 bytes at a time (chip's FIFO size).
			This appends a 4 byte header to be compatible with the RadioHead library.
			The header defaults to using the initialized attributes:
				* (destination,node,identifier,flags) --> 1 byte each
				* It may be temporarily overidden via the kwargs - destination,node,identifier,flags.
				* Values passed via kwargs do not alter the attribute settings.
			The keep_listening argument should be set to True if you want to start listening
			automatically after the packet is sent. The default setting is False.

			Returns: True if success or False if the send timed out. """
		assert 0 < len(data) <= 60
		self.__idle()  # Stop receiving to clear FIFO and keep it clear.
		# Fill the FIFO with a packet to send. Combine header and data to form payload
		payload = bytearray(4)
		# payload[0] = 4 + len(data) # already using variable data_length datagram
		if destination is None:  # use attribute
			payload[0] = self.destination
		else:  # use kwarg
			payload[0] = destination
		if node is None:  # use attribute
			payload[1] = self.node
		else:  # use kwarg
			payload[1] = node
		if identifier is None:  # use attribute
			payload[2] = self.identifier
		else:  # use kwarg
			payload[2] = identifier
		if flags is None:  # use attribute
			payload[3] = self.flags
		else:  # use kwarg
			payload[3] = flags
		payload = payload + data
		# Write payload to transmit fifo
		self.spi_write_fifo( payload )
		# Turn on transmit mode to send out the packet.
		self.__transmit()
		# Wait for packet sent interrupt with explicit polling (not ideal but
		# best that can be done right now without interrupts).
		timed_out = check_timeout(self.__packet_sent, self.xmit_timeout)
		# Listen again if requested.
		if keep_listening:
			self.__listen()
		else:  # Enter idle mode to stop receiving other packets.
			self.__idle()
		return not timed_out

	def send_with_ack(self, data):
		""" Reliable Datagram mode: Send a packet with data and wait for an ACK response.
			The packet header is automatically generated.
			If enabled, the packet transmission will be retried on failure """
		if self.ack_retries:
			retries_remaining = self.ack_retries
		else:
			retries_remaining = 1

		got_ack = False
		self.sequence_number = (self.sequence_number + 1) & 0xFF
		while not got_ack and retries_remaining:
			self.identifier = self.sequence_number
			self.send(data, keep_listening=True)
			# Don't look for ACK from Broadcast message
			if self.destination == _RH_BROADCAST_ADDRESS:
				got_ack = True
			else:
				# wait for a packet from our destination (get the fata with header)
				ack_packet = self.receive(timeout=self.ack_wait, with_header=True)
				if ack_packet is not None:
					if ack_packet[3] & _RH_FLAGS_ACK: # Is this a Ack packet for the packet we did sent
						if ack_packet[2] == self.identifier: # check the ID
							got_ack = True
							break
			# pause before next retry -- random delay
			if not got_ack:
				# delay by random amount before next try
				sleep(self.ack_wait + self.ack_wait * random.random())
			retries_remaining = retries_remaining - 1
			# set retry flag in packet header
			self.flags |= _RH_FLAGS_RETRY
		self.flags = 0  # clear flags
		return got_ack

	def receive( self, *, keep_listening=True, with_ack=False, timeout=None, with_header=False ):
		""" Wait to receive a packet from the receiver. If a packet is found the payload bytes
			are returned, otherwise None is returned (which indicates the timeout elapsed with no reception). """
		# If keep_listening is True (the default) the chip will immediately enter listening mode
		# after reception of a packet, otherwise it will fall back to idle mode and ignore any future reception.
		# All packets must have a 4 byte header for compatibilty with the RadioHead library.
		#   - The header consists of 4 bytes (To,From,ID,Flags).
		#     The default setting will  strip the header before returning the packet to the caller.
		#   - If with_header is True then the 4 byte header will be returned with the packet.
		#     The payload then begins at packet[4].
		#   - If with_ack is True, send an ACK after receipt (Reliable Datagram mode)
		timed_out = False
		if timeout is None:
			timeout = self.receive_timeout
		if timeout is not None:
			# Wait for the payload_ready signal.  This is not ideal and will
			# surely miss or overflow the FIFO when packets aren't read fast
			# enough, however it's the best that can be done from Python without
			# interrupt supports.
			# Make sure we are listening for packets.
			self.__listen()
			timed_out = check_timeout(self.__payload_ready, timeout)
		# Payload ready is set, a packet is in the FIFO.
		packet = None
		# save last RSSI reading
		self.last_rssi = self.rssi
		# Enter idle mode to stop receiving other packets.
		self.__idle()
		if not timed_out:
			# Read the length of the FIFO.
			fifo_length = self.spi_read(RFM69_REG_FIFO)
			# Handle if the received packet is too small to include the 4 byte
			# RadioHead header and at least one byte of data --reject this packet and ignore it.
			if fifo_length > 0:  # read and clear the FIFO if anything in it
				packet = self.spi_burst_read(RFM69_REG_FIFO, fifo_length)

			if fifo_length < 5:
				packet = None
			else:
				if ( self.node != _RH_BROADCAST_ADDRESS
					and packet[0] != _RH_BROADCAST_ADDRESS
					and packet[0] != self.node  ):
					packet = None
				# send ACK unless this was an ACK or a broadcast
				elif ( with_ack
					and ((packet[3] & _RH_FLAGS_ACK) == 0)
					and (packet[0] != _RH_BROADCAST_ADDRESS)   ):
					# delay before sending Ack to give receiver a chance to get ready
					if self.ack_delay is not None:
						time.sleep(self.ack_delay)
					# send ACK packet to sender (data is b'!')
					self.send( b"!", destination=packet[1], node=packet[0],
							identifier=packet[2], flags=(packet[3] | _RH_FLAGS_ACK),  )
					# reject Retries if we have seen this identifier from this source before
					if (self.seen_ids[packet[1]] == packet[2]) and (packet[3] & _RH_FLAGS_RETRY):
						packet = None
					else:  # save the packet identifier for this source
						self.seen_ids[packet[1]] = packet[2]
				if ( not with_header and packet is not None ):  # skip the header if not wanted
					packet = packet[4:]
		# Listen again if necessary and return the result packet.
		if keep_listening:
			self.__listen()
		else:
			# Enter idle mode to stop receiving other packets.
			self.__idle()
		return packet

	def __transmit(self):
		""" Transmit a packet which is queued in the FIFO.  This is a low level function for
			entering transmit mode and more.  For generating and transmitting a packet of data use """
		# Like RadioHead library, turn on high power boost if enabled.
		if self._tx_power >= 18:
			self.spi_write( RFM69_REG_TEST_PA1, RF_TEST_PA1_BOOST)
			self.spi_write( RFM69_REG_TEST_PA2, RF_TEST_PA2_BOOST)
		# Enable packet sent interrupt for D0 line.
		self.dio_0_mapping = 0b00
		# Enter TX mode (will clear FIFO!).
		#self.operation_mode = TX_MODE
		self.set_mode( RFM69_MODE_TX )


	def __idle(self):
		"""Enter idle standby mode (switching off high power amplifiers if necessary)."""
		# Like RadioHead library, turn off high power boost if enabled.
		if self._tx_power >= 18:
			self.spi_write( RFM69_REG_TEST_PA1, RF_TEST_PA1_NORMAL)
			self.spi_write( RFM69_REG_TEST_PA2, RF_TEST_PA2_NORMAL)
		#self.operation_mode = STANDBY_MODE
		self.set_mode( RFM69_MODE_STDBY )

	def __sleep(self):
		""" Enter sleep mode. """
		#self.operation_mode = SLEEP_MODE
		self.set_mode( RFM69_MODE_SLEEP )

	def __listen(self):
		"""Listen for packets to be received by the chip.  Use :py:func:`receive` to listen, wait and retrieve packets as they're available. """
		# Like RadioHead library, turn off high power boost if enabled.
		if self._tx_power >= 18:
			self.spi_write( RFM69_REG_TEST_PA1, RF_TEST_PA1_NORMAL)
			self.spi_write( RFM69_REG_TEST_PA2, RF_TEST_PA2_NORMAL)
		# Enable payload ready interrupt for D0 line.
		self.dio_0_mapping = 0b01
		# Enter RX mode (will clear FIFO!).
		#self.operation_mode = RX_MODE
		self.set_mode( RFM69_MODE_RX )

	def __packet_sent(self):
		""" Transmit status """
		return (self.spi_read(RFM69_REG_IRQ_FLAGS2) & 0x8) >> 3

	def __payload_ready(self):
		""" Receive status """
		return (self.spi_read(RFM69_REG_IRQ_FLAGS2) & 0x4) >> 2

	def clear_fifo( self ):
		self.set_mode( RFM69_MODE_STDBY )
		self.set_mode( RFM69_MODE_RX )

	@property
	def temperature( self ):
		""" internal chip temperature in °C. Not calibrated and not very accurate.
			WARNING: reading temp stops receiving/sending """
		oldMode = self._mode

		self.set_mode( RFM69_MODE_STDBY )
		self.spi_write( RFM69_REG_TEMP1, RF_TEMP1_MEAS_START )

		while self.spi_read( RFM69_REG_TEMP1 ) == RF_TEMP1_MEAS_RUNNING:
			pass

		rawTemp = self.spi_read( RFM69_REG_TEMP2 )
		self.set_mode( oldMode )
		return (168 - rawTemp) - 5 # Offset and compensate for self-heating

	@property
	def rx_bw_dcc_freq( self ):
		return (self.spi_read( RFM69_REG_RX_BW ) & 0b11100000) >> 5

	@rx_bw_dcc_freq.setter
	def rx_bw_dcc_freq( self, value ):
		reg =  self.spi_read( RFM69_REG_RX_BW ) & 0b00011111
		self.spi_write( RFM69_REG_RX_BW, reg | (value<<5))

	@property
	def rx_bw_mantissa( self ):
		return (self.spi_read( RFM69_REG_RX_BW ) & 0b00011000) >> 3

	@rx_bw_mantissa.setter
	def rx_bw_mantissa( self, value ):
		reg = self.spi_read( RFM69_REG_RX_BW ) & 0b11100111
		self.spi_write( RFM69_REG_RX_BW, reg | (value<<3))

	@property
	def rx_bw_exponent( self ):
		return self.spi_read( RFM69_REG_RX_BW ) & 0b00000111

	@rx_bw_exponent.setter
	def rx_bw_exponent( self, value ):
		reg = self.spi_read( RFM69_REG_RX_BW ) & 0b11111000
		self.spi_write( RFM69_REG_RX_BW, reg | value )

	@property
	def afc_bw_dcc_freqs( self ):
		return ( self.spi_read( RFM69_REG_AFC_BW ) & 0b11100000 ) >> 5

	@afc_bw_dcc_freqs.setter
	def afc_bw_dcc_freqs( self, value ):
		reg = self.spi_read( RFM69_REG_AFC_BW ) & 0b00011111
		self.spi_write( RFM69_REG_AFC_BW, reg | (value<<5) )

	@property
	def afc_bw_mantissa( self ):
		return ( self.spi_read( RFM69_REG_AFC_BW ) & 0b00011000 ) >> 3

	@afc_bw_mantissa.setter
	def afc_bw_mantissa( self, value ):
		reg = self.spi_read( RFM69_REG_AFC_BW ) & 0b11100111
		self.spi_write( RFM69_REG_AFC_BW, reg|(value << 3) )

	@property
	def afc_bw_exponent( self ):
		return self.spi_read( RFM69_REG_AFC_BW ) & 0b00000111

	@afc_bw_exponent.setter
	def afc_bw_exponent( self, value ):
		reg = self.spi_read( RFM69_REG_AFC_BW ) & 0b11111000
		self.spi_write( RFM69_REG_AFC_BW, reg | value )

	@property
	def packet_format( self ):
		return self.spi_read( RFM69_REG_PACKET_CONFIG1 ) >> 7

	@packet_format.setter
	def packet_format( self, value  ):
		reg = self.spi_read( RFM69_REG_PACKET_CONFIG1 ) & 0b01111111
		self.spi_write( RFM69_REG_PACKET_CONFIG1, reg | (value<<7) )

	@property
	def dc_free( self ):
		return (self.spi_read( RFM69_REG_PACKET_CONFIG1 ) & 0b01100000) >> 5

	@dc_free.setter
	def dc_free( self, value ):
		reg = self.spi_read( RFM69_REG_PACKET_CONFIG1 ) & 0b10011111
		self.spi_write( RFM69_REG_PACKET_CONFIG1, reg | (value << 5) )

	@property
	def crc_on( self ):
		return (self.spi_read( RFM69_REG_PACKET_CONFIG1 ) & 0b00010000) >> 4

	@crc_on.setter
	def crc_on( self, value ):
		reg = self.spi_read( RFM69_REG_PACKET_CONFIG1 ) & 0b11101111
		self.spi_write( RFM69_REG_PACKET_CONFIG1, reg | (value << 4) )

	@property
	def crc_auto_clear_off( self ):
		return ( self.spi_read( RFM69_REG_PACKET_CONFIG1 ) & 0b00001000 ) >> 3

	@crc_auto_clear_off.setter
	def crc_auto_clear_off( self, value ):
		reg = self.spi_read( RGM69_REG_PACKET_CONFIG1 ) & 0b11110111
		self.spi_write( RGM69_REG_PACKET_CONFIG1, reg | (value<<3) )

	@property
	def address_filter( self ):
		return (self.spi_read( RFM69_REG_PACKET_CONFIG1 ) & 0b00000110 ) >> 1

	@address_filter.setter
	def address_filter( self, value ):
		reg = self.spi_read( RFM69_REG_PACKET_CONFIG1 ) & 0b11111001
		self.spi_write( RFM69_REG_PACKET_CONFIG1, reg | (value << 1) )

	@property
	def aes_on( self ):
		return self.spi_read( RFM69_REG_PACKET_CONFIG2 ) & 0b00000001

	@aes_on.setter
	def aes_on( self, value ):
		reg = self.spi_read( RFM69_REG_PACKET_CONFIG2 ) & 0b11111110
		self.spi_write( RFM69_REG_PACKET_CONFIG2, reg | value )

	@property
	def encryption_key(self):
		""" The AES encryption key used to encrypt and decrypt packets by the chip. This can be set
			to None to disable encryption (the default), otherwise it must be a 16 byte long byte
			string which defines the key (both the transmitter and receiver must use the same key value). """
		# Handle if encryption is disabled.
		if self.aes_on == 0:
			return None
		# Encryption is enabled so read the key and return it.
		key = self.spi_burst_read(RFM69_REG_AES_KEY1, 16)
		return key

	@encryption_key.setter
	def encryption_key(self, val):
		# Handle if unsetting the encryption key (None value).
		if val is None:
			self.aes_on = 0
		else:
			# Set the encryption key and enable encryption.
			assert len(val) == 16
			self.spi_write(RFM69_REG_AES_KEY1, val)
			self.aes_on = 1

	@property
	def rssi( self ):
		""" The received strength indicator (in dBm).
			May be inaccuate if not read immediatey. last_rssi contains the value read immediately receipt of the last packet. """
		# Read RSSI register and convert to value using formula in datasheet.
		return -self.spi_read(RFM69_REG_RSSI_VALUE) / 2.0

	def sample_rssi(self): # TODO: check
		""" Make a request to radio module for sampling the rssi. Must only be called in RX mode.
		 	(Not tested yet)"""
		if (self._mode != RFM69_MODE_RX ):
			# Not sure what happens otherwise, so check this
			return 0
		# Trigger RSSI Measurement
		self.spi_write( RFM69_REG_RSSI_CONFIG, RF_RSSI_START )
		# Wait for Measurement to complete
		while (self.spi_read(RFM69_REG_RSSI_CONFIG) & RF_RSSI_DONE) != RF_RSSI_DONE:
			pass

		# Read, store in _lastRssi and return RSSI Value
		self.last_rssi = self.rssi
		return self.last_rssi

	# Read/Write Functions
	def spi_read(self, register):
		# Read U8 register from module
		data = bytearray(2)
		data[0] = register & ~0x80
		data[1] = 0
		resp = bytearray(2)
		self.nss.low()
		self.spi.write_readinto(data, resp ) # timeout=5000)
		self.nss.high()
		return resp[1]

	def spi_burst_read(self, register, length):
		data = bytearray(length+1)
		data[0] = register & ~0x80
		for i in range(1,length+1):
			data[i] = 0
		# We get the length again as the first character of the buffer
		buf = bytearray(length+1)
		self.nss.low()
		self.spi.write_readinto(data, buf ) # , timeout=5000)
		self.nss.high()
		return buf[1:]

	def spi_write(self, register, value):
		# Write U8 value into a module register
		if (type(value) is bytearray) or (type(value) is bytes):
			data = bytearray(1)
			data[0] = register | 0x80
			self.nss.low()
			self.spi.write(data )# , timeout=5000)
			self.spi.write(value)
			self.nss.high()
		else:
			data = bytearray(2)
			data[0] = register | 0x80
			data[1] = value
			self.nss.low()
			self.spi.write(data )# , timeout=5000)
			self.nss.high()

	def spi_write_fifo(self, data):
		# fifo_data = bytearray(len(data)+2)
		buf2 = bytearray(2)
		buf2[0] = RFM69_REG_FIFO | 0x80
		buf2[1] = len(data )
		self.nss.low()
		self.spi.write( buf2 )
		self.spi.write( data )
		self.nss.high()


	@property
	def dio_0_mapping( self ):
		""" DIO mapping allow to set the G0 as Interrupt Pin when packet is sent/received """
		# _RegisterBits(_REG_DIO_MAPPING1, offset=6, bits=2)
		return (self.spi_read( RFM69_REG_DIO_MAPPING1 ) & 0b11000000) >> 6

	@dio_0_mapping.setter
	def  dio_0_mapping( self, value ):
		assert 0<=value<=3, "Invalid DIO_0 value"
		reg = self.spi_read( RFM69_REG_DIO_MAPPING1 ) & 0b11000000
		self.spi_write( RFM69_REG_DIO_MAPPING1, reg | (value<<6) )

	@property
	def frequency_mhz( self ):
		"""The frequency of the radio in Megahertz. Only the allowed values for your radio must be specified (i.e. 433 vs. 915 mhz)! """
		# FRF register is computed from the frequency following the datasheet.
		# See section 6.2 and FRF register description.
		# Read bytes of FRF register and assemble into a 24-bit unsigned value.
		msb = self.spi_read( RFM69_REG_FRF_MSB )
		mid = self.spi_read( RFM69_REG_FRF_MID )
		lsb = self.spi_read( RFM69_REG_FRF_LSB )
		frf = ((msb << 16) | (mid << 8) | lsb) & 0xFFFFFF
		frequency = (frf * _FSTEP) / 1000000.0
		return frequency

	@frequency_mhz.setter
	def frequency_mhz(self, val):
		assert 290 <= val <= 1020
		# Calculate FRF register 24-bit value using section 6.2 of the datasheet.
		frf = int((val * 1000000.0) / _FSTEP) & 0xFFFFFF
		# Extract byte values and update registers.
		msb = frf >> 16
		mid = (frf >> 8) & 0xFF
		lsb = frf & 0xFF
		self.spi_write( RFM69_REG_FRF_MSB, msb)
		self.spi_write( RFM69_REG_FRF_MID, mid)
		self.spi_write( RFM69_REG_FRF_LSB, lsb)


	@property
	def frequency_deviation(self):
		"""The frequency deviation in Hertz. Freq Shift = 2x deviation"""
		msb = self.spi_read( RFM69_REG_FDEV_MSB)
		lsb = self.spi_read( RFM69_REG_FDEV_LSB)
		return _FSTEP * ((msb << 8) | lsb)

	@frequency_deviation.setter
	def frequency_deviation(self, val):
		assert 0 <= val <= (_FSTEP * 16383)  # fdev is a 14-bit unsigned value
		# Round up to the next closest integer value with addition of 0.5.
		fdev = int((val / _FSTEP) + 0.5) & 0x3FFF
		self.spi_write( RFM69_REG_FDEV_MSB, fdev >> 8)
		self.spi_write( RFM69_REG_FDEV_LSB, fdev & 0xFF)

	@property
	def bitrate(self):
		"""The modulation bitrate in bits/second (or chip rate if Manchester encoding is enabled).
		   Can be a value from ~489 to 32mbit/s, but see the datasheet for the exact supported values. """
		msb = self.spi_read( RFM69_REG_BITRATE_MSB )
		lsb = self.spi_read( RFM69_REG_BITRATE_LSB )
		return _FXOSC / ((msb << 8) | lsb)

	@bitrate.setter
	def bitrate(self, val):
		assert (_FXOSC / 65535) <= val <= 32000000.0
		# Round up to the next closest bit-rate value with addition of 0.5.
		bitrate = int((_FXOSC / val) + 0.5) & 0xFFFF
		self.spi_write( RFM69_REG_BITRATE_MSB, bitrate >> 8)
		self.spi_write( RFM69_REG_BITRATE_LSB, bitrate & 0xFF)

	@property
	def sync_on( self ):
		""" See sync_word() """
		# sync_on = _RegisterBits(_REG_SYNC_CONFIG, offset=7)
		return self.spi_read( RFM69_REG_SYNC_CONFIG ) >> 7

	@sync_on.setter
	def sync_on( self, value ):
		""" See sync_word() """
		# sync_on = _RegisterBits(_REG_SYNC_CONFIG, offset=7)
		reg = self.spi_read( RFM69_REG_SYNC_CONFIG ) & 0b01111111
		reg = reg | (1 if value else 0)<<7
		self.spi_write( RFM69_REG_SYNC_CONFIG, reg )

	@property
	def sync_size( self ):
		# sync_size = _RegisterBits(_REG_SYNC_CONFIG, offset=3, bits=3)
		return (self.spi_read( RFM69_REG_SYNC_CONFIG ) & 0b00111000) >> 3

	@sync_size.setter
	def sync_size( self, value ):
		assert 0<=value<=7
		# sync_size = _RegisterBits(_REG_SYNC_CONFIG, offset=3, bits=3)
		reg = self.spi_read( RFM69_REG_SYNC_CONFIG ) & 0b11000111
		reg = reg | (value << 3)
		self.spi_write( RFM69_REG_SYNC_CONFIG, reg )

	@property
	def sync_word(self):
		"""The synchronization word value (8 bytes long, 64 bits)  which indicates the synchronization word for transmitted and received packets. Any
		received packet which does not include this sync word will be ignored.
		Setting a value of None will disable synchronization word matching entirely. """
		# Handle when sync word is disabled..
		if not self.sync_on:
			return None
		# Sync word is not disabled so read the current value.
		sync_word_length = self.sync_size + 1  # Sync word size is offset by 1 according to datasheet .
		# sync_word = bytearray(sync_word_length)
		# self._read_into(RFM69_REG_SYNC_VALUE1, sync_word)
		return self.spi_burst_read( RFM69_REG_SYNC_VALUE1, sync_word_length )

	@sync_word.setter
	def sync_word(self, val):
		# Handle disabling sync word when None value is set.
		if val is None:
			self.sync_on = 0
		else:
			# Check sync word is at most 8 bytes.
			assert 1 <= len(val) <= 8
			# Update the value, size and turn on the sync word.
			self.spi_write( RFM69_REG_SYNC_VALUE1, val )
			self.sync_size = len(val) - 1  # Again sync word size is offset by
			# 1 according to datasheet.
			self.sync_on = 1

	@property
	def preamble_length(self):
		"""The length of the preamble for sent and received packets, an unsigned 16-bit value.
		Received packets must match this length or they are ignored! Set to 4 to match the
		RadioHead RFM69 library.
		"""
		msb = self.spi_read( RFM69_REG_PREAMBLE_MSB )
		lsb = self.spi_read( RFM69_REG_PREAMBLE_LSB )
		return ((msb << 8) | lsb) & 0xFFFF

	@preamble_length.setter
	def preamble_length( self, val ):
		assert 0 <= val <= 65535
		self.spi_write( RFM69_REG_PREAMBLE_MSB, (val >> 8) & 0xFF)
		self.spi_write( RFM69_REG_PREAMBLE_LSB, val & 0xFF)

	@property
	def output_power( self ):
		""" Return the raw register value. See tx_power instead """
		# _RegisterBits(_REG_PA_LEVEL, offset=0, bits=5)
		return self.spi_read( RFM69_REG_PA_LEVEL ) & 0x1F

	@property
	def tx_power(self):
		""" Transmit power in dBm. Can be set to a value from -2 to 20 for high power devices
		(RFM69HCW, high_power=True) or -18 to 13 for low power devices. Only integer power
		levels are actually set (i.e. 12.5 will result in a value of 12 dBm).
		"""
		# Follow table 10 truth table from the datasheet for determining power
		# level from the individual PA level bits and output power register.
		#   pa_0_on = _RegisterBits(_REG_PA_LEVEL, offset=7)
		#   pa_1_on = _RegisterBits(_REG_PA_LEVEL, offset=6)
		#   pa_2_on = _RegisterBits(_REG_PA_LEVEL, offset=5)
		val = self.spi_read( RFM69_REG_PA_LEVEL )
		pa0 = (val & 0b10000000) > 0
		pa1 = (val & 0b01000000) > 0
		pa2 = (val & 0b00100000) > 0
		if pa0 and not pa1 and not pa2:
			# -18 to 13 dBm range
			return -18 + self.output_power
		if not pa0 and pa1 and not pa2:
			# -2 to 13 dBm range
			return -18 + self.output_power
		if not pa0 and pa1 and pa2 and not self.high_power:
			# 2 to 17 dBm range
			return -14 + self.output_power
		if not pa0 and pa1 and pa2 and self.high_power:
			# 5 to 20 dBm range
			return -11 + self.output_power
		raise RuntimeError("Power amplifiers in unknown state!")

	@tx_power.setter
	def tx_power(self, val):
		""" eg: use 13 dBm """
		val = int(val)
		# Determine power amplifier and output power values depending on
		# high power state and requested power.
		pa_0_on = 0
		pa_1_on = 0
		pa_2_on = 0
		output_power = 0
		if self.high_power:
			# Handle high power mode.
			assert -2 <= val <= 20
			if val <= 13:
				pa_1_on = 1
				output_power = val + 18
			elif 13 < val <= 17:
				pa_1_on = 1
				pa_2_on = 1
				output_power = val + 14
			else:  # power >= 18 dBm
				# Note this also needs PA boost enabled separately!
				pa_1_on = 1
				pa_2_on = 1
				output_power = val + 11
		else:
			# Handle non-high power mode.
			assert -18 <= val <= 13
			# Enable only power amplifier 0 and set output power.
			pa_0_on = 1
			output_power = val + 18
		# Set power amplifiers and output power as computed above.
		# 3 higher bits are pa_x_on, 5 lower bits are output_power
		# value = self.spi_read( RFM69_REG_PA_LEVEL ) & 0b00011111
		pa_value = (pa_0_on<<7) | (pa_1_on<<6) | (pa_2_on<<5)
		self._tx_power = pa_value | output_power
		self.spi_write( RFM69_REG_PA_LEVEL, self._tx_power )


# === Testing code ===
#from machine import SPI, Pin
#spi = SPI(0, baudrate=50000, polarity=0, phase=0, firstbit=SPI.MSB)
#nss = Pin( 5, Pin.OUT, value=True )
#rst = Pin( 3, Pin.OUT, value=False )
