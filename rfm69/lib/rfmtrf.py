""" rfmtrf.py - transfer helper for stream

Designed to manage data stream larger than 60 bytes (so over RFM69 capacity)
Relies on the radiohead capabilities.

RFM69HCW breakout : https://shop.mchobby.be/product.php?id_product=1390
RFM69HCW breakout : https://www.adafruit.com/product/3071

see project: https://github.com/mchobby/esp8266-upy/tree/master/rfm69
"""
from micropython import const
import time

F_NONE    = const( 0x0 )
F_RESET   = const( 0xF ) # Reinit at destination
F_EXIT    = const( 0xE ) # destination must exit process
F_SET_REG = const( 0x1 )
F_GET_REG = const( 0x2 )
F_DATA    = const( 0x3 ) # packets contains data
F_LASTERR = const( 0x7 ) # Used to get the error status at destination

REG_SERVICE = const( 0x00 ) # Register for service


SVC_FILE_TRANSFERT = const( 0x01 )

class RfmToolBase:
	def __init__( self, rfm ):
		self.rfm = rfm
		self._last_error = 0 # Handled at destination. Returned at F_LASTERR request

	def is_flag( self, packet, value ):
		return packet[3] == value

	def data_to_bytes( self, value ):
		if type( value ) is str:
			return bytes(value, "utf-8")
		if type( value ) is int:
			if value <= 255:
				return bytes([value])
		raise Exception( "data_to_bytes: Type not supported." )

	def set_register( self, register, value ):
		""" set a register at destination """
		assert 0x00<=register<=0xFF
		data = self.data_to_bytes( value )
		self.rfm.flags = self.rfm.flags | F_SET_REG
		if not self.rfm.send_with_ack( bytes( [register] ) + data ):
			raise Exception("set_register %s comm error" % register )

	def get_last_error( self ):
		""" Request last error at destination. 0 = OK, -1 = not received, >0 = error from destination """
		self.rfm.flags = F_LASTERR
		if not self.rfm.send_with_ack( b"\x00" ):
			raise Exception("get_last_error() %s comm error" % flag )
		packet = self.rfm.receive( with_ack=True, timeout=5 ) # We should receive the information within 5 seconds!
		if packet==None:
			return -1 # we have communication error
		return packet[0] # contains the error code

	def send_last_error( self, to_node ):
		""" return the last error to get_last_error """
		if self.rfm.ack_delay: # Gives some time to get_last_error to be ready
			time.sleep(self.ack_delay)
		self.rfm.destination = to_node
		_r = self.rfm.send_with_ack( bytes([self._last_error]) )
		self.last_error = 0
		return _r

	def get_register( self, reg ):
		""" Request a register value to the destination. """
		assert 0<= reg <= 255
		self.rfm.flags = F_GET_REG
		if not self.rfm.send_with_ack( bytes([reg]) ):
			raise Exception("get_reg_value() %s comm error" % reg )
		packet = self.rfm.receive( with_ack=True, timeout=5 ) # We should receive the information within 5 seconds!
		if packet==None:
			return -1 # we have communication error
		return packet # contains register data

	def send_reg_value( self, to_node, value ):
		""" Send the register value to the callee (also reset last error) """
		if self.rfm.ack_delay: # Gives some time to get_last_error to be ready
			time.sleep(self.ack_delay)
		self.rfm.destination = to_node
		_r = self.rfm.send_with_ack( self.data_to_bytes(value) )
		self.last_error = 0
		return _r

	def set_flag( self, flag ):
		""" Send a flag at destination """
		self.rfm.flags = flag
		if not self.rfm.send_with_ack( b"\x00" ):
			raise Exception("set_flag() %s comm error" % flag )

	@property
	def last_error(self):
		return self._last_error

	@last_error.setter
	def last_error(self, value ):
		assert 0<= value <= 255
		self._last_error = value


class StreamSender( RfmToolBase ):
	def __init__( self, rfm, destination ):
		""" Send the stream (a file) to the destination node over the rfm interface"""
		super().__init__( rfm )
		self.destination = destination


	def send( self, filename, stream, with_exit=False ):
		if self.rfm.node == 0xFF: # broadcast
			raise Exception( 'Node has no address!' )
		self.rfm.destination = self.destination
		# request the service at destinatory
		value = self.get_register( REG_SERVICE ) # return the value as bytes
		if value[0] != SVC_FILE_TRANSFERT:
			raise Exception( 'Invalid service at listener side')
		self.set_flag( F_RESET ) # Ensure that destination does reset
		self.set_register( 0x01, filename )
		self.set_register( 0x0A, 0x01 ) # Start Data Transfert
		# Check for error code
		err = self.get_last_error() # Request last error at destination
		if err != 0:
			raise Exception('Fails to start transfer. Err %i' % err )



		if with_exit:
			self.set_flag( F_EXIT ) # Destination exits process

class StreamReceiver( RfmToolBase ):
	def __init__( self, rfm, svc_id ):
		""" Receive a Stream (a file) over the rfm interface"""
		super().__init__( rfm )
		self.service_id = svc_id
		self.reset()

	def reset( self ):
		self.filename = ''
		self.counter = 0


	def listen( self ):
		while True:
			print('.')
			packet = self.rfm.receive( with_ack=True, with_header=True, timeout=2 )
			if packet == None:
				continue
			if self.is_flag( packet, F_SET_REG ):
				reg  = packet[4]
				data = packet[5:]
				print( 'SET_REG',reg,data)
				if reg==0x01:
					self.filename = str( data, "ascii" )
				elif reg==0x0A: # Transfer Command Register
					if data[0] == 0x01:
						# Check that everything is OK and open the file in Write Mode
						if self.filename == '':
							self.last_error = 0x10
							continue
						# TODO: open the file
					elif data[0] == 0x02: # File transfer terminated
						# TODO: close the file
						pass
					else:
						self.last_error = 0x11
			elif self.is_flag( packet, F_GET_REG ):
				reg  = packet[4]
				print( 'GET_REG',reg )
				if reg==0x00:
					_r = self.send_reg_value( to_node=packet[1], value=self.service_id ) # the identification of service
				elif reg==0x01:
					_r = self.send_reg_value( to_node=packet[1], value=self.filename ) # the file to store
				else:
					_r = self.send_reg_value( to_node=packet[1], value="This is a test" ) # return the register value
				if not _r:
					print( 'send_reg_value() failed' )
				continue
			elif self.is_flag( packet, F_RESET ):
				print( 'RESET' )
				self.reset()
			elif self.is_flag( packet, F_DATA ):
				print( 'DATA', packet )
			elif self.is_flag( packet, F_EXIT ):
				print( 'EXIT' )
				break
			elif self.is_flag( packet, F_LASTERR ):
				print( 'LASTERR' )
				if not self.send_last_error( to_node=packet[1] ): # Send last error to receiver
					print( 'send_last_err() failed' )
			else:
				print( 'Flag %s not supported' % packet[3] )
