""" RFID/NFC pn532 driver for MicroPython

  HAL (Hardware Abstraction Layer) for UART communication with PN532 module.

Sponsor
* Lycee Francais Jean-Monnet, Bruxelles, Belgique

Author(s):
* Meurisse D for MC Hobby sprl

See Github: https://github.com/mchobby/esp8266-upy/tree/master/pn532-rfid
"""
# Based on https://github.com/elechouse/PN532/blob/PN532_HSU/PN532_HSU/PN532_HSU.h

from machine import UART
from pn_intf import *

class PN_UART:
	def __init__( self, UART_ID, timeout=5000 ):
		self.ser = UART( UART_ID, baudrate=115200, timeout=timeout ) # 8n1, PN532_HSU_READ_TIMEOUT=1000
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
		# Returns: 0 when ACK frame received OTHERWISE returns ErrorCode
		self.clear_rx()

		self.command = header[0]
		#print("write_command: ", self.command)

		self.ser.write( bytes([PN532_PREAMBLE,PN532_STARTCODE1,PN532_STARTCODE2]) )
		l = len(header)+1 # length of data field: TFI + DATA
		if body!=None:
			l+=len(body)

		_l = 0xFF ^ l # ~L+1 = one's complement of L + 1
		_l = (_l+1) & 0xFF # contraint into uint8_t
		self.ser.write( bytes([l, _l, PN532_HOSTTOPN532]) ) # Length, checksum of length = ~l+1, ...
		sum = PN532_HOSTTOPN532 # sum of TFI + DATA (uint_8)
		self.ser.write( header )

		for data in header:
			sum = (sum + data) & 0xFF

		if body!=None:
			self.ser.write( body )
			for data in body:
				sum = (sum + data) & 0xFF

		checksum = (0xFF^sum)+1 #  checksum =  ~sum + 1 for TFI + DATA
		checksum = checksum & 0xFF # Contraint uint8_t
		self.ser.write( bytes([checksum, PN532_POSTAMBLE]) )

		return self.read_ack_frame()

	def read_response( self, buf, blen=None ): # int16_t
		#print( "read_response: enter")
		if blen==None:
			blen = len(buf)

		# Frame Preamble and Start Code
		if self.receive(self.buf3)<=0 :
			# print( "read_response: Timeout")
			return PN532_TIMEOUT

		if (self.buf3[0] != 0) or (self.buf3[1] != 0) or (self.buf3[2] != 0xFF):
			#print( "read_response: Invalid_Frame")
			return PN532_INVALID_FRAME

		# receive length and check
		_buf = memoryview(self.buf3)
		if self.receive( _buf[0:2] ) <= 0:
			#print( "read_response: Timeout 2")
			return PN532_TIMEOUT

		if ((self.buf3[0] + self.buf3[1]) & 0XFF ) !=0 :
			# print("read_response: Length error")
			return PN532_INVALID_FRAME

		self.buf3[0] -= 2
		_readlen = self.buf3[0]
		# print( "read_response: _readlen=", _readlen )
		if _readlen > blen :
			# print("read_response: PN532_NO_SPACE not enough space")
			return PN532_NO_SPACE

		# receive command byte
		cmd = self.command + 1 # expected response command
		# print( "read_response: expect cmd %s @ [1] for next read" % cmd )
		if self.receive( _buf[0:2] ) <= 0 :
			# print( "read_response: Timeout 3")
			return PN532_TIMEOUT

		if (self.buf3[0] != PN532_PN532TOHOST) or (self.buf3[1] != cmd):
			# print("read_response: Command error");
			return PN532_INVALID_FRAME

		_readbuf = memoryview(buf)
		if self.receive( _readbuf[0:_readlen] ) != _readlen:
			# print( "read_response: Timeout 4")
			return PN532_TIMEOUT

		sum = (PN532_PN532TOHOST + cmd) & 0xFF
		for i in range(_readlen):
			sum = (sum + buf[i]) & 0xFF

		# checksum and postamble
		if self.receive( _buf[0:2] ) <= 0 :
			# print( "read_response: Timeout 5")
			return PN532_TIMEOUT

		if( (sum + self.buf3[0]) & 0xFF != 0 ) or (self.buf3[1] != 0):
			# print("read_response: Checksum error")
			return PN532_INVALID_FRAME

		#print( "read_response: OK with _readlen=", _readlen)
		return _readlen

	def read_ack_frame( self ):
		# Returns: 0=OK otherwise Error Code
		#print( "read_ack_frame: Enter" )
		if self.receive( self.buf6, len(self.buf6) ) <= 0:
			return PN532_TIMEOUT;
		#print( "read_ack_frame: buf6=", self.buf6 )

		if any( [ val != (0,0,0xFF,0,0xFF,0)[idx] for idx, val in enumerate(self.buf6) ] ):
			return PN532_INVALID_ACK;

		#print( "read_ack_frame: OK" )
		return 0


	def receive( self, buf, _len=None  ):
		#print( "receive: enter" )
		to_read = _len if _len!=None else len(buf)
		_r = self.ser.readinto( buf, to_read ) # read until count or time_out is reach
		if (_r==None) or (_r < to_read):
			#print( "receive: timeout" )
			return PN532_TIMEOUT
		#print( "receive: readed %s with buf %s" % (_r,buf) )
		return _r
