""" RFID/NFC pn532 driver for MicroPython

  Very rough implementation of MiFare Library for MicroPython
  -- DO NOT USE -- DO NOT USE -- DO NOT USE -- DO NOT USE --

  Kept for historical reason.

Sponsor
* Lycee Francais Jean-Monnet, Bruxelles, Belgique

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/pn532-rfid
"""
from machine import UART
from pn_const import *
from pn_intf import *

# Based on https://github.com/elechouse/PN532/blob/PN532_HSU/PN532_HSU/PN532_HSU.h
class PN_UART:
	def __init__( self, UART_ID ):
		self.ser = UART( UART_ID, baudrate=115200, timeout=1000) # 8n1, PN532_HSU_READ_TIMEOUT=1000
		self.command = 0 # Last command used in write_command()
		self.buf6 = bytearray( 6 )
		self.buf3 = bytearray( 3 )
		self.buf64 = bytearray( 64 )

	def clear_rx( self ):
		#  Empty Serial Input buffer
		while self.ser.any() > 0:
			self.ser.read()
			pass

	def wake_up( self ):
		self.ser.write( bytes([0x55,0x55,0,0,0] ) )
		self.clear_rx()

	def write_command( self, header, body=None ): # const uint8_t *header, uint8_t hlen, const uint8_t *body, uint8_t blen)
		# Header and body are bytes() structures
		self.clear_rx()

		self.command = header[0]
		print("command", self.command)

		self.ser.write( bytes([PN532_PREAMBLE,PN532_STARTCODE1,PN532_STARTCODE2]) )
		l = len(header)+1 # length of data field: TFI + DATA
		if body!=None:
			l+=len(body)
		# ~L+1 = one's complement of L + 1
		_l = 0xFF ^ l
		_l = (_l+1) & 0xFF # contraint into uint8_t
		print( l, _l, PN532_HOSTTOPN532 )
		self.ser.write( bytes([l, _l, PN532_HOSTTOPN532]) ) # Length, checksum of length = ~l+1, ...
		sum = PN532_HOSTTOPN532 # sum of TFI + DATA (uint_8)
		self.ser.write( header )

		#_serial->write(header, hlen);
		#for (uint8_t i = 0; i < hlen; i++) {
		#	sum += header[i];
		#
		#	DMSG_HEX(header[i]);
		#}
		for data in header:
			sum = (sum + data) & 0xFF

		if body!=None:
			self.ser.write( body )
			#for (uint8_t i = 0; i < blen; i++) {
			#	sum += body[i];
			#
			#	DMSG_HEX(body[i]);
			#}
			for data in body:
				sum = (sum + data) & 0xFF

		#uint8_t checksum = ~sum + 1;
		checksum = (0xFF^sum)+1 #  checksum of TFI + DATA
		checksum = checksum & 0xFF # Contraint uint8_t
		self.ser.write( bytes([checksum, PN532_POSTAMBLE]) )

		return self.read_ack_frame()

	def read_response( self, buf, blen=None ): # int16_t
		if blen==None:
			blen = len(buf)

		# Frame Preamble and Start Code
		if self.receive(self.buf3)<=0 :
			print( "read_response: Timeout")
			return PN532_TIMEOUT

		if (self.buf3[0] != 0) or (self.buf3[1] != 0) or (self.buf3[2] != 0xFF):
			print( "read_response: Invalid_Frame")
			return PN532_INVALID_FRAME

		# receive length and check
		_buf = memoryview(self.buf3)
		if self.receive( _buf[0:2] ) <= 0:
			print( "read_response: Timeout 2")
			return PN532_TIMEOUT

		if ((self.buf3[0] + self.buf3[1]) & 0XFF ) !=0 :
			print("Length error")
			return PN532_INVALID_FRAME

		self.buf3[0] -= 2
		_readlen = self.buf3[0]
		if _readlen > blen :
			print("PN532_NO_SPACE not enough space")
			return PN532_NO_SPACE

		# receive command byte
		cmd = self.command + 1 # expected response command
		if self.receive( _buf[0:2] ) <= 0 :
			print( "read_response: Timeout 3")
			return PN532_TIMEOUT

		if (self.buf3[0] != PN532_PN532TOHOST) or (self.buf3[1] != cmd):
			print("Command error");
			return PN532_INVALID_FRAME

		_readbuf = memoryview(buf)
		#if receive(buf, length[0], timeout) != length[0] {
		#	return PN532_TIMEOUT;
		if self.receive( _readbuf[0:_readlen] ) != _readlen:
			print( "read_response: Timeout 4")
			return PN532_TIMEOUT

		sum = (PN532_PN532TOHOST + cmd) & 0xFF
		for i in range(_readlen):
			sum = (sum + buf[i]) & 0xFF

		# checksum and postamble
		if self.receive( _buf[0:2] ) <= 0 :
			print( "read_response: Timeout 5")
			return PN532_TIMEOUT

		if( (sum + self.buf3[0]) & 0xFF != 0 ) or (self.buf3[1] != 0):
			print("Checksum error")
			return PN532_INVALID_FRAME

		print( "read_response: _readlen", _readlen)
		return _readlen

	def read_ack_frame( self ):
		# const uint8_t PN532_ACK[] = {0, 0, 0xFF, 0, 0xFF, 0};
		#uint8_t ackBuf[sizeof(PN532_ACK)];

		#DMSG("\nAck: ");

		#if( receive(ackBuf, sizeof(PN532_ACK), PN532_ACK_wake_upIT_TIME) <= 0 ){
		#    DMSG("Timeout\n");
		#    return PN532_TIMEOUT;
		#}
		print( "buf6", self.buf6 )
		if self.receive( self.buf6, len(self.buf6) ) <= 0:
			return PN532_TIMEOUT;
		print( "read_ack_frame", self.buf6 )

		if any( [ val != (0,0,0xFF,0,0xFF,0)[idx] for idx, val in enumerate(self.buf6) ] ):
			return PN532_INVALID_ACK;

		return 0

	def receive( self, buf, _len=None  ):
		print( "enter receive", buf, len )
		to_read = _len if _len!=None else len(buf)
		_r = self.ser.readinto( buf, to_read ) # read until count or time_out is reach
		print( "to_read",to_read,"data",buf)
		if _r < to_read:
			return PN532_TIMEOUT
		else:
			return _r

class PN532:
	# See https://github.com/elechouse/PN532/blob/PN532_HSU/PN532/PN532.cpp
	def __init__( self, hal_interface ):
		self._hal = hal_interface # HArdware abstraction layer to communicate with PN532
		self.pn532_packetbuffer = bytearray( 64 )
		# uint8_t _uid[7];  // ISO14443A uid
		# uint8_t _uidLen;  // uid len
		# uint8_t _key[6];  // Mifare Classic key
		# uint8_t inListedTag; // Tg number of inlisted tag.
		# uint8_t _felicaIDm[8]; // FeliCa IDm (NFCID2)
		# uint8_t _felicaPMm[8]; // FeliCa PMm (PAD)


	def begin( self ):
		self._hal.wake_up()

	def getFirmwareVersion( self ):
		#uint32_t response;
		self.pn532_packetbuffer[0] = PN532_COMMAND_GETFIRMWAREVERSION

		mv_command = memoryview( self.pn532_packetbuffer )
		if self._hal.write_command( mv_command[:1] ) != 0:
			return 0;

		# read data packet
		# int16_t status = HAL(readResponse)(pn532_packetbuffer, sizeof(pn532_packetbuffer));
		status = self._hal.read_response( mv_command[:] )
		print( "getFirmwareVersion: status", status)
		if status < 0:
			return 0
		# if (0 > status) {
		#    return 0;
		# }
		#
		response = self.pn532_packetbuffer[0]
		response <<= 8
		response |= self.pn532_packetbuffer[1]
		response <<= 8
		response |= self.pn532_packetbuffer[2]
		response <<= 8
		response |= self.pn532_packetbuffer[3]
		#
		return response

	@property
	def firmware_version( self ):
		_val = self.getFirmwareVersion()
		_chipset = "pn5%s" % hex((_val>>24)&0xFF).replace('0x','')
		_firmversion = "%s.%s" % ( (versiondata>>16) & 0xFF, (versiondata>>8) & 0xFF )
		return {"CHIPSET":_chipset, "FIRMWARE":_firmversion}



uart_hal = PN_UART( 1 ) # Using PN532 over UART

nfc = PN532( uart_hal )
nfc.begin()
versiondata = nfc.getFirmwareVersion()
print( versiondata )
print( nfc.firmware_version )
