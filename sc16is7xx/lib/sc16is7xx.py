""" sc16is7xx MicroPython Library 

  The SC16IS740, SC16IS750, SC16IS760 are SPI/I2C to UART interface.
  Those have 64 bytes FiFo.

  Usual Oscillator are 1843200 Hz (1.8432 Mhz, DEFAULT) or 3072000 Hz (3.072 Mhz).
  Frequency can be change at SC16IS7XX creation with "oscillator_hz" parameter.


* Author(s): Meurisse D.
* See https://github.com/mchobby/esp8266-upy/sc16is7xx 

Producing driver is a tedeous work made available to you as free software!
Help us to produce more code and purchase your products from shop.mchobby.be
"""

# SPI must have the following configuration
# * SPI.MSB most Significative bit first 
# * polarity = 0
# * phase = 0
#
from micropython import const
from machine import SPI, I2C, idle, Pin
import time

TX_CHUNCK_SIZE = const( 8 )

REG_RHR  = const( 0x00 ) # read only  : Receive Holding Register
REG_THR  = const( 0x00 ) # write only : Transmit Holding Registeer
REG_IER  = const( 0x01 ) # read/write : Interrupt Enable Register
REG_FCR  = const( 0x02 ) # write only : FIFO Control Register
REG_LCR  = const( 0x03 ) # read/write : Line Control Register
REG_MCR  = const( 0x04 ) # read/write : Modem Control Register
REG_LSR  = const( 0x05 ) # read only  : Line Status Register
REG_MSR  = const( 0x06 ) # read only  : Modem Status Register
REG_SPR  = const( 0x07 ) # read/write : Scratch Pad Register
REG_TXLVL= const( 0x08 ) # read only  : Transmiter FIFO Level Register
REG_RXLVL= const( 0x09 ) # read only  : Receiver FIFO Level Register
REG_EFCR = const( 0x0F ) # read/write : Extra Features Control Register

LCR_SPECIAL_START = const(0x80)
LCR_SPECIAL_END 	= const(0xbf)

FCR_INIT_VALUE = const( 0x07 ) # Clear TX FIFOs, Clear RX Fifo, Enable FiFo
FCR_RX_LEVEL = { 8:0, 16:1, 56:2, 60:3 } # characters
FCR_TX_LEVEL = { 8:0, 16:1, 32:2, 56:3 } # spaces


# Burst reads on the serial interface (that is, reading multiple elements 
# on the I2C-bus without a STOP or repeated START condition, or reading multiple
# elements on the SPI bus without de-asserting the CS pin), should not be
# performed on the IIR register.
REG_IIR  = const( 0x02 ) # read only  :  Interrupt Identification Register

# Accessible when MCR[2]=1 and EFR[4]=1
REG_TCR  = const( 0x06 ) # read/write : Transmission Control Register
REG_TLR  = const( 0x07 ) # read/write : Trigger Level Register

# ONLY for SC16IS750/SC16IS760
REG_IODIR  = const( 0x0A ) # read/write : I/O Direction register
REG_IOSTATE= const( 0x0B ) # read/write : I/O State Register
REG_IOINENA= const( 0x0C ) # read/write : I/O Interrupt Enable
REG_IOCTRL = const( 0x0E ) # read/write : I/O Control Register

# SPECIAL REGISTER SET
# accessible when LCR[7]=1 and not 0xBF
REG_DLL  = const( 0x00 ) # read/write : Division Register (Low)
REG_DLH  = const( 0x01 ) # read/write : Division Register (High)

# ENHANCED FEATURE REGISTERS 
# accessible when LCR=0xBF
REG_EFR  = const( 0x02 ) # read/write : Enhanced Features Register
REG_XON1 = const( 0x04 ) # read/write : 
REG_XON2 = const( 0x05 ) # read/write : 
REG_XOFF1= const( 0x06 ) # read/write : 
REG_XOFF2= const( 0x07 ) # read/write : 

# Software Workflow
NO_WORKFLOW = const( 0b00 ) # None is also accepted
XON1_XOFF1  = const( 0b10 )
XON2_XOFF2  = const( 0b01 )
XON1_OR_XON2_XOFF1_OR_XOFF2   = const( 0b1111 ) # Only for RX
XON1_AND_XON2_XOFF1_AND_XOFF2 = const( 0b1011 ) # only for TX

# IRQ Source identification
CTS_RTS_IRQ   = const( 16 ) # HIGHEST PRIORITY. RTS pin or CTS pin change state from active (LOW) to inactive (HIGH).
XOFF_IRQ      = const(  8 ) # Receive Xoff character(s)/ special character. Cleared by Xon.
PIN_IRQ       = const( 24 ) # => MUST read the pin status. Input pins change of state
MODEM_IRQ     = const(  0 ) # => MUST read modem status. Change of state of modem input pins
TX_LEVEL_IRQ  = const(  1 ) # Transmit FIFO empty (FIFO disable) or TX FIFO passes above trigger level (FIFO enable)
RX_LEVEL_IRQ  = const(  2 ) # Receive data ready (FIFO disable) or RX FIFO above trigger level (FIFO enable)
RX_TIMEOUT_IRQ= const(  6 ) # Stale data in RX FIFO
RX_LINE_ERROR = const(  3 ) # LOWEST PRIORITY. OE, FE, PE, or BI errors occur in characters in the RX FIFO

# Enabling Interrupt
CST_INT  = const( 0b10000000 ) 
RTS_INT  = const( 0b01000000 )
XOFF_INT = const( 0b00100000 ) 
SLEEP_INT= const( 0b00010000 ) # Sleep Mode
MODEM_INT= const( 0b00001000 ) # Modem Status Interrupt
LINE_INT = const( 0b00000100 ) # Receive Line Status interrupt
TX_INT   = const( 0b00000010 ) # Transmit Holding Register interrupt
RX_INT   = const( 0b00000001 ) # Receive Holding Register interrupt


# ============================================
#
#    Bus Access Wrapper 
#
# ============================================
# Transmit SC16IS7XX call over the SPI/I2C bus
# by using the appropriate SC16IS7XX protocol

class BusWrapper():
	def __init__( self, bus, cs_pin=None, address=None, rst_pin=None, **kwargs ):
		# Bus can be SPI or I2C instance. cs_pin is required for SPI bus, 
		# address is required for the I2C bus 
		self.bus = bus
		if isinstance( bus, SPI ):
			assert cs_pin!=None, "cs_pin required for SPI bus"
		elif not isinstance( bus, I2C ):
			raise Exception( "bus must be I2C or SPI")
		self.cs_pin = cs_pin
		self.address= address
		if rst_pin != None:
			rst_pin.value(0)
			time.sleep_ms(1)
			rst_pin.value(1)


	# Common method that must be implemented in descendant
	def write_reg( self, reg, value, ch ):
		# ch is the Channel
		raise NotImplementedError()

	def read_reg( self, reg, ch ):
		raise NotImplementedError()

	def write_fifo( self, ch, buf ):
		raise NotImplementedError()

	def read_fifo( self, ch, nbytes ):
		# Returns a bytes() object
		raise NotImplementedError()


class SPIWrapper( BusWrapper ):
	def __init__( self, **kwargs ):
		super().__init__( **kwargs )
		self.buf2 = bytearray(2)
		self.buf_tx = bytearray(1)
		self.buf_rx = bytearray(1)


	def write_reg( self, reg, value, ch ):
		assert 0<=reg<=15, "Invalid address range %i (0..15)" % reg
		assert (0<=ch<=2), "Invalid channel %i" % ch 
		self.buf2[0] = 0x00 + (reg<<3) + (ch<<1) 
		self.buf2[1] = value  
		self.cs_pin.value(0)
		self.bus.write( self.buf2 )
		# print( "write_reg", hex(reg), "value", hex(value) , "=>", bin(self.buf2[0]), bin(self.buf2[1]) ) 
		self.cs_pin.value(1)

	def read_reg( self, reg, ch ):
		assert 0<=reg<=15, "Invalid address range %i (0..15)" % reg
		assert (0<=ch<=2), "Invalid channel %i" % ch
		self.buf_tx[0] = 0x80 + (reg<<3) + (ch<<1)  
		self.buf_rx[0] = 0x00
		self.cs_pin.value(0)
		self.bus.write( self.buf_tx )
		self.bus.readinto( self.buf_rx )
		self.cs_pin.value(1)
		# print( "read_reg", hex(reg), "=", hex(self.buf_rx[0]), bin(self.buf_rx[0]) )
		return int(self.buf_rx[0]) 

	def write_fifo( self, ch, buf ):
		assert (0<=ch<=2), "Invalid channel %i" % ch
		self.buf_tx[0] = 0b00000000 + (ch<<1)
		self.cs_pin.value(0)
		self.bus.write( self.buf_tx )
		self.bus.write( buf )
		self.cs_pin.value(1)

	def read_fifo( self, ch, nbytes ):
		assert (0<=ch<=2), "Invalid channel %i" % ch
		self.buf_tx[0] = 0b10000000 + (ch<<1)
		self.cs_pin.value(0)
		self.bus.write( self.buf_tx )
		_r = self.bus.read( nbytes )
		self.cs_pin.value(1)
		return _r 


class I2CWrapper( BusWrapper ):
	def __init__( self, **kwargs ):
		super().__init__( **kwargs )
		raise NotImplementedError( "I2C Support not yet implemented")


# ============================================
#
#    UartAdapter
#
# ============================================
# Expose UART interface to user code
# Translate UART call to SC16IS7XX via the bus_wrapper

class UartAdapter():
	def __init__( self, owner, ch ):
		self.owner = owner # ref to the SC16IS7XX owner
		self.ch    = ch # The SC16ISXX channel
		self.baudrate = None
		self.timeout  = 1000 # ms timeout for first char
		self.timeout_char= 100 # ms timeout between chars
		self.__start = 0 # Timer Start (in ms)
		self.__xonoff_defined = False # True when xon/xoff chars are defined with define_xon_xoff()
		

	def init( self, **kwargs ):
		# kwargs contains the UART parameters as machine.UART().init()
		self.baudrate = kwargs['baudrate']

		# See Arduino code @ https://github.com/rickkas7/SC16IS740RK/tree/master
		# oscillator KC3225K1.84320C1GE00
		# OSC XO 1.8432MHz CMOS SMD $1.36
		# https://www.digikey.com/product-detail/en/avx-corp-kyocera-corp/KC3225K1.84320C1GE00/1253-1488-1-ND/5322590
		# Another suggested frequency from the data sheet is 3.072 MHz
		# 
		# Can also see https://github.com/tunerok/SC16IS750_SC16IS740_simple_driver/tree/main
		if 'timeout' in kwargs:
			self.timeout = kwargs['timeout']
		if 'timeout_char' in kwargs:
			self.timeout_char = kwargs['timeout_char']

		# The divider devices the clock frequency to 16x the baud rate
		_div = int(self.owner.oscillator_hz / (self.baudrate * 16))


		self.owner.bus_wrapper.write_reg(REG_LCR, LCR_SPECIAL_START, ch=self.ch)  # 0x80
		self.owner.bus_wrapper.write_reg(REG_DLL, _div & 0xff, ch=self.ch)
		self.owner.bus_wrapper.write_reg(REG_DLH, _div >> 8, ch=self.ch)
		self.owner.bus_wrapper.write_reg(REG_LCR, LCR_SPECIAL_END, ch=self.ch) # 0xbf

		# Grab UART configuration
		_bits = 8
		_parity = None
		_stop = 1
		if 'bits' in kwargs:
			_bits = kwargs['bits']
		if 'parity' in kwargs:
			_parity = kwargs['parity']
		if 'stop' in kwargs:
			_stop = kwargs['stop']

		# Encode word length
		_options = 0x0
		if _bits==5:
			_options += 0b00
		elif _bits==6:
			_options += 0b01
		elif _bits==7:
			_options += 0b10
		elif _bits==8:
			_options += 0b11
		else:
			raise ValueError( 'bits can be in range 5..8' )

		# Encode stop bit
		if _stop==1:
			_options += 0b000
		if _stop==1.5:
			if _bits!=5:
				raise ValueError( '1.5 stop bits only possible for 5 data bits')
			_options += 0b100
		elif _stop==2:
			if _bits<=6:
				raise ValueError( 'Invalid 2 stop bits for %s data bits' % _bits )
			_options += 0b100

		# Encode Parity
		if _parity==None:
			_options += 0b000000
		elif _parity==0: # Even
			_options += 0b011000
		elif _parity==1: # Odd 
			_options += 0b001000
		elif _parity==10: # forced 0
			_options += 0b111000
		elif _parity==11: # forced 1
			_options += 0b101000
		else:
			raise ValueError( 'Invalid parity %s value' % _parity )

		# for 8N1 the _options will be 0b000011
		self.owner.bus_wrapper.write_reg(REG_LCR, _options & 0x3f, ch=self.ch)

		# Enable FIFOs
		self.owner.bus_wrapper.write_reg( REG_FCR, FCR_INIT_VALUE, ch=self.ch) # Clear TX FIFOs, Clear RX Fifo, Enable FiFo
		time.sleep_ms(1) # Reset requires minimum waiting of 2*Tclk


	def deinit( self ):
		pass 


	# --- SC16IS7XX Specific ------------------------------
	#
	# -----------------------------------------------------

	def dump_regs( self ):
		# Returns a list of register = value
		_l = []
		for reg in (0x00,0x01,0x02,0x03,0x04,0x05,0x06,0x07,0x08,0x09,0x0F):
			_l.append( (reg, self.owner.bus_wrapper.read_reg( reg, ch=self.ch )) ) # add tuple (reg,value)
		return _l

	def auto_rts( self, halt_trigger, resume_trigger ):
		assert 4<=halt_trigger<=60, "RTS trigger must be within 4-60 range"
		assert 4<=resume_trigger<=60, "RTS trigger must be within 4-60 range"
		assert (halt_trigger%4) + (resume_trigger%4) == 0, "Trigger level are step by 4!"
		assert halt_trigger > resume_trigger, "halt_trigger must be greater than resume_trigger!"

		# Set the 
		_halt = halt_trigger//4
		_resume = resume_trigger//4

		# cannot enable auto-RTS if RS485 is configured to use it
		_efcr = self.owner.bus_wrapper.read_reg( REG_EFCR, ch=self.ch )
		if (_efcr and 0b00010000) > 0:
			raise Exception("RTS already managed by RS485!")		
		
		# Set LCR=0xBF to access EFR register
		_old_lcr = self.owner.bus_wrapper.read_reg( REG_LCR, ch=self.ch ) # store transmission config (eg: 8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, 0xBF, ch=self.ch )

		# activate enhanced feature
		_efr = self.owner.bus_wrapper.read_reg(REG_EFR, ch=self.ch)
		try:
			if (_efr & 0b00001111)>0 :
				raise Exception("Soft flow control already setup!")
			_efr = _efr | 0b00010000
			self.owner.bus_wrapper.write_reg(REG_EFR, _efr, ch=self.ch)
		except:
			# Close access to EFR & restore transmission config (eg:8n1)
			self.owner.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=self.ch )
			raise

		# Close access to EFR & restore transmission config (eg:8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=self.ch )


		# Enable TCR & TLR register access
		_mcr = self.owner.bus_wrapper.read_reg(REG_MCR, ch=self.ch)
		_mcr = _mcr | 0b00000100
		self.owner.bus_wrapper.write_reg(REG_MCR, _mcr, ch=self.ch)

		# Set TCR trigger values
		_tcr = self.owner.bus_wrapper.read_reg(REG_TCR, ch=self.ch)
		_tcr = _tcr | (_resume<<4)
		_tcr = _tcr | _halt
		self.owner.bus_wrapper.write_reg(REG_TCR, _tcr, ch=self.ch)

		# TLR must be cleared (to use TCR)
		self.owner.bus_wrapper.write_reg(REG_TLR, 0x00, ch=self.ch)

		# Disable TCR & TLR register access
		_mcr = self.owner.bus_wrapper.read_reg(REG_MCR, ch=self.ch)
		_mcr = _mcr & 0b11111011
		self.owner.bus_wrapper.write_reg(REG_MCR, _mcr, ch=self.ch)

		self.owner.bus_wrapper.write_reg( REG_LCR, 0xBF, ch=self.ch )

		# Enable auto RTS flow control
		_efr = _efr | 0b01000000
		self.owner.bus_wrapper.write_reg(REG_EFR, _efr, ch=self.ch)		

		# Close access to EFR & restore transmission config (eg:8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=self.ch )

		# Initial State of RTS bit in Modem (MCR)
		#_mcr = self.owner.bus_wrapper.read_reg( REG_MCR, ch=self.ch )
		#_mcr = _mcr | 0x02 
		#self.owner.bus_wrapper.write_reg( REG_MCR, _mcr, ch=self.ch )

	def auto_cts( self ):
		# Set LCR=0xBF to access EFR register
		_old_lcr = self.owner.bus_wrapper.read_reg( REG_LCR, ch=self.ch ) # store transmission config (eg: 8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, 0xBF, ch=self.ch )

		# Enable auto CTS flow control
		_efr = self.owner.bus_wrapper.read_reg(REG_EFR, ch=self.ch)
		_efr = _efr | 0b10000000
		self.owner.bus_wrapper.write_reg(REG_EFR, _efr, ch=self.ch)		

		# Close access to EFR & restore transmission config (eg:8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=self.ch )

	def any_tx( self ):
		# Number of chars in the TX FiFo
		return 	64-(self.owner.bus_wrapper.read_reg( REG_TXLVL, self.ch ) & 0x7F)


	def define_xon_xoff( self, xon, xoff, xon2=None, xoff2=None ):
		assert xon!=xoff, "Invalid XON/XOFF values" 
		if (xon2!=None) or (xoff2!=None):
			assert (xon2!=None) and (xoff2!=None) and (xon2!=xoff2), "Invalid XON2/XOFF2 values"

		# Set LCR=0xBF to access XON/XOFF registers
		_old_lcr = self.owner.bus_wrapper.read_reg( REG_LCR, ch=self.ch ) # store transmission config (eg: 8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, 0xBF, ch=self.ch )

		self.owner.bus_wrapper.write_reg( REG_XON1, xon, ch=self.ch )
		self.owner.bus_wrapper.write_reg( REG_XOFF1, xoff, ch=self.ch )
		if (xon2!=None) or (xoff2!=None):
			self.owner.bus_wrapper.write_reg( REG_XON2, xon2, ch=self.ch )
			self.owner.bus_wrapper.write_reg( REG_XOFF2, xoff2, ch=self.ch )

		# Close access to EFR & restore transmission config (eg:8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=self.ch )
		self.__xonoff_defined = True


	def auto_xon_xoff( self, halt_trigger, resume_trigger, flow_rx, flow_tx ):
		assert 4<=halt_trigger<=60, "RTS trigger must be within 4-60 range"
		assert 4<=resume_trigger<=60, "RTS trigger must be within 4-60 range"
		assert (halt_trigger%4) + (resume_trigger%4) == 0, "Trigger level are step by 4!"
		assert halt_trigger > resume_trigger, "halt_trigger must be greater than resume_trigger!"
		assert (flow_rx+flow_tx)>0, "At least one of the flow_rx, flow_tx must be defined"
		assert self.__xonoff_defined , "xon/xoff must be defined first!"

		# Set the level
		_halt = halt_trigger//4
		_resume = resume_trigger//4

		# Transform None --> No Workflow 
		if flow_rx==None:
			flow_rx = NO_WORKFLOW
		if flow_tx==None:
			flow_tx = NO_WORKFLOW

		# Special constant are use for FULL MEANING/DESCRIPTION of the operation
		if ( flow_tx in (NO_WORKFLOW,XON1_XOFF1,XON2_XOFF2,XON1_AND_XON2_XOFF1_AND_XOFF2) ) and  \
		   ( flow_rx in (NO_WORKFLOW,XON1_XOFF1,XON2_XOFF2) ):
		   pass # Combinations allowed
		elif ( flow_tx in (XON1_XOFF1,XON2_XOFF2) ) and (flow_rx==XON1_OR_XON2_XOFF1_OR_XOFF2):
			pass # Combinations alloweds
		elif (flow_tx in (XON1_AND_XON2_XOFF1_AND_XOFF2,NO_WORKFLOW)) and (flow_rx==XON1_AND_XON2_XOFF1_AND_XOFF2):
			pass # combination alloweds
		else:
			raise Exception( "Invalid combination of rx and tx workflows" )

		# reduce the xxx_AND_xxx & xxx_OR_xxx to the allowed register value
		if flow_tx==XON1_AND_XON2_XOFF1_AND_XOFF2:
			flow_tx = flow_tx & 0b11 
		if flow_rx in (XON1_OR_XON2_XOFF1_OR_XOFF2, XON1_AND_XON2_XOFF1_AND_XOFF2):
			flow_rx = flow_rx & 0b11

		# Compute _workflow value
		_workflow = (flow_tx<<2) | flow_rx	


		# cannot enable auto-RTS if RS485 is configured to use it
		_efcr = self.owner.bus_wrapper.read_reg( REG_EFCR, ch=self.ch )
		if (_efcr and 0b00010000) > 0:
			raise Exception("Flow control already managed by RS485!")		
		
		# Set LCR=0xBF to access EFR register
		_old_lcr = self.owner.bus_wrapper.read_reg( REG_LCR, ch=self.ch ) # store transmission config (eg: 8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, 0xBF, ch=self.ch )

		# activate enhanced feature
		_efr = self.owner.bus_wrapper.read_reg(REG_EFR, ch=self.ch)
		try:
			if (_efr & 0b11000000)>0 :
				raise Exception("Hardware flow control already setup!")
			_efr = _efr | 0b00010000
			self.owner.bus_wrapper.write_reg(REG_EFR, _efr, ch=self.ch)
		except:
			# Close access to EFR & restore transmission config (eg:8n1)
			self.owner.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=self.ch )
			raise

		# Close access to EFR & restore transmission config (eg:8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=self.ch )

		# Enable TCR & TLR register access
		_mcr = self.owner.bus_wrapper.read_reg(REG_MCR, ch=self.ch)
		_mcr = _mcr | 0b00000100
		self.owner.bus_wrapper.write_reg(REG_MCR, _mcr, ch=self.ch)

		# Set TCR trigger values
		_tcr = self.owner.bus_wrapper.read_reg(REG_TCR, ch=self.ch)
		_tcr = _tcr | (_resume<<4)
		_tcr = _tcr | _halt
		self.owner.bus_wrapper.write_reg(REG_TCR, _tcr, ch=self.ch)

		# TLR must be cleared (to use TCR)
		self.owner.bus_wrapper.write_reg(REG_TLR, 0x00, ch=self.ch)

		# Disable TCR & TLR register access
		_mcr = self.owner.bus_wrapper.read_reg(REG_MCR, ch=self.ch)
		_mcr = _mcr & 0b11111011
		self.owner.bus_wrapper.write_reg(REG_MCR, _mcr, ch=self.ch)

		self.owner.bus_wrapper.write_reg( REG_LCR, 0xBF, ch=self.ch )

		# Enable auto Software flow control
		_efr = _efr | (0b00001111 & _workflow )
		self.owner.bus_wrapper.write_reg(REG_EFR, _efr, ch=self.ch)		

		# Close access to EFR & restore transmission config (eg:8n1)
		self.owner.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=self.ch )


	# --- Machine.UART implementation ---------------------
	#
	# -----------------------------------------------------
	def any( self ):
		""" UART.any() 
		Returns number of chars available to read. 0 or >1 """
		return self.owner.bus_wrapper.read_reg( REG_RXLVL, self.ch ) & 0x7F


	def write( self, buf ):
		""" UART.write( buf ) """
		# Write by chunck for 8 bytes
		assert isinstance( buf, (bytes,bytearray,memoryview)), "buf doesn't support buffer protocol!"
		# slice transmission buffer
		icount = len(buf)//TX_CHUNCK_SIZE + (1 if len(buf)%TX_CHUNCK_SIZE>0 else 0)
		for i in range( icount ):
			_slice = buf[i*TX_CHUNCK_SIZE:(i+1)*TX_CHUNCK_SIZE]
			# wait to have to room in the FiFo
			while (self.owner.bus_wrapper.read_reg( REG_TXLVL, self.ch ) & 0x7F) < TX_CHUNCK_SIZE:
				idle()
			self.owner.bus_wrapper.write_fifo( self.ch, _slice )
			

	def read( self, nbytes=None ):
		""" UART.read( nbytes=None ) returns a buffer """
		self.__start = time.ticks_ms()
		self.__last_char = None
		_r = None
		while True:
			if self.__start==None:
				self.__start = time.ticks_ms()
			elif time.ticks_diff(time.ticks_ms(),self.__start)>self.timeout:
				break
			icount = self.owner.bus_wrapper.read_reg( REG_RXLVL, self.ch ) & 0x7F
			if icount>0: # We have content
				if _r==None:
					_r=bytearray()
				# how many can we pop 
				_count = icount if nbytes==None else min( nbytes-len(_r), icount )
				for by in self.owner.bus_wrapper.read_fifo( self.ch, _count ):
					_r.append(by)
				self.__last_char = time.ticks_ms()
				# filled?
				if (nbytes!=None) and (len(_r)==nbytes):
					break # it's time to exit!
			# next char timeout
			if ( self.__last_char!=None ) and ( time.ticks_diff( time.ticks_ms(), self.__last_char ) > self.timeout_char ):
				break
		return _r


	def readline( self ):
		""" UART.readline() """
		self.__start = time.ticks_ms()
		self.__last_char = None
		_r = bytearray() # readed bytes
		while True:
			if self.__start==None:
				self.__start = time.ticks_ms()
			elif time.ticks_diff(time.ticks_ms(),self.__start)>self.timeout:
				break
			icount = self.owner.bus_wrapper.read_reg( REG_RXLVL, self.ch ) & 0x7F
			for i in range(icount):
				by = self.owner.bus_wrapper.read_fifo( self.ch, 1 )				
				_r.append( by[0] )
				if by[0]==10: # \n
					return _r
				self.__last_char = time.ticks_ms()				
			# next char timeout
			if ( self.__last_char!=None ) and ( time.ticks_diff( time.ticks_ms(), self.__last_char ) > self.timeout_char ):
				break
		# return result
		if len(_r)==0:
			return None
		return _r
		

	def readinto( self, buf, nbytes=None ):
		""" UART.readinto( buf, nbytes=None ) """
		assert isinstance( buf, bytearray), "buf doesn't support buffer protocol!"
		assert (nbytes==None) or (nbytes<=len(buf)), "nbytes larger than buffer"
		self.__start = time.ticks_ms()
		self.__last_char = None
		_pos = 0 # index where the next value will be stored
		while True:
			if self.__start==None:
				self.__start = time.ticks_ms()
			elif time.ticks_diff(time.ticks_ms(),self.__start)>self.timeout:
				break
			icount = self.owner.bus_wrapper.read_reg( REG_RXLVL, self.ch ) & 0x7F
			if icount>0: # We have content
				# how many can we pop 
				_count = min( icount, len(buf)-_pos) if nbytes==None else min( nbytes-_pos, icount )
				for by in self.owner.bus_wrapper.read_fifo( self.ch, _count ):
					buf[_pos]=by
					_pos += 1
				self.__last_char = time.ticks_ms()
				# filled?
				if (nbytes!=None) and (_pos>=nbytes):
					break # it's time to exit!
				elif (nbytes==None) and (_pos>=len(buf)):
					break
			# next char timeout
			if ( self.__last_char!=None ) and ( time.ticks_diff( time.ticks_ms(), self.__last_char ) > self.timeout_char ):
				break
		# Number of bytes copied
		return _pos if _pos>0 else None


	def txdone( self ):
		""" UART.txdone() """
		# Returns True when everything is sent
		# REG_TXLVL number of space available in TX FIFO
		return (self.owner.bus_wrapper.read_reg( REG_TXLVL, self.ch ) & 0x7F )==64 # 64 byte free in TXFifo

	def flush( self ):
		""" UART.flush() """
		# Wait until everything is sent.
		# Should be sensitive to timeout except when flow control is activated
		self.__start = time.ticks_ms()
		while not self.txdone():
			if time.ticks_diff( time.ticks_ms(), self.__start ) > self.timeout:
				raise Exception( 'Send timeout!' )
			idle()

	def sendbreak( self, time_ms=None ):
		""" UART.sendbreak() """
		us_per_bit = 1000000 / self.baudrate # 9600 bauds --> 104 uSec
		# Calculate the minimum sendbreak time (for sending 1 char)
		# Time for 9bits, 2 stop bits, 1 parity bit, 1 start bit = 13 bit
		us_wait_time = int(us_per_bit * 13)

		val = self.owner.bus_wrapper.read_reg( REG_LCR, ch=self.ch )
		# set break bit
		val = val | (1<<6)
		self.owner.bus_wrapper.write_reg( REG_LCR, val, ch=self.ch )

		if time_ms==None:
			time.sleep_us(us_wait_time)
		else:
			time.sleep_ms(time_ms)
			print('Sleep_ms', time_ms)

		# clear break bit
		val = val & 0b10111111
		self.owner.bus_wrapper.write_reg( REG_LCR, val, ch=self.ch )


# ============================================
#
#    PinAdapter
#
# ============================================
# Expose Pin interface to user code
# Translate Pin call to SC16IS7XX via the bus_wrapper

class PinAdapter():
	def __init__( self, owner, id ):		
		assert 0<= id <=7, "Invalid Pin ID %s" % id
		self.owner = owner # ref to the SC16IS7XX owner		
		self.id = id # ID is the GPIO number 

	def init( self, **kwargs ):
		# kwargs contains the UART parameters as machine.UART().init()
		self.mode = kwargs['mode']
		assert self.mode in (Pin.IN, Pin.OUT), "Only Pin.In, Pin.Out mode are allowed!"
		self._initial_value = None
		if 'value' in kwargs:
			self._initial_value = kwargs['value']

		_iodir = self.owner.bus_wrapper.read_reg( REG_IODIR, ch=0 ) 
		if self.mode==Pin.IN:
			# set the bit to 0
			_iodir = _iodir & (0xFF ^ (1<<self.id))
			self.owner.bus_wrapper.write_reg( REG_IODIR, _iodir, ch=0 )
		else:
			# Set the bit to 1
			_iodir = _iodir | (1<<self.id) 
			self.owner.bus_wrapper.write_reg( REG_IODIR, _iodir, ch=0 )

		if self._initial_value != None:
			self.value( self._initial_value )


	def value( self, state=None ):
		_iostate = self.owner.bus_wrapper.read_reg( REG_IOSTATE, ch=0 )
		if state==None: # read the state
			return 1 if (_iostate & (1<<self.id))>0 else 0
		else: # write the state			
			if state: # Set the bit
				_iostate = _iostate | (1<<self.id)
			else:
				_iostate = _iostate & ( 0xFF ^ (1<<self.id))
			self.owner.bus_wrapper.write_reg( REG_IOSTATE, _iostate, ch=0 )

	def enable_irq(self, state=True):
		# Enable IRQ generation for Input GPIO
		# IRQ will resets when the value is read!
		_intena =  self.owner.bus_wrapper.read_reg( REG_IOINENA, ch=0 )
		if state==True:
			_intena = _intena | (1<<self.id)
		else:
			_intena = _intena & (0xFF ^ (1<<self.id))
		self.owner.bus_wrapper.write_reg( REG_IOINENA, _intena, ch=0 )



# ============================================
#
#    SC16IS7XX Base Class
#
# ============================================

class SC16IS7XX():
	def __init__( self, **kwargs ):
		self.bus_wrapper = None
		self.oscillator_hz = 1843200 # Default 
		if 'oscillator_hz' in kwargs:
			self.oscillator_hz = kwargs['oscillator_hz']

		# bus can be I2C or SPI, cs_pin only required for SPI
		if isinstance(kwargs['bus'],SPI):
			self.bus_wrapper = SPIWrapper( **kwargs )
		else:
			self.bus_wrapper = I2CWrapper( **kwargs )
	

	def get_uart( self, ch, **kwargs ):
		# Get an UartAdapter on the given SC16IS7xxx channel 
		assert (0<=ch<=2), "Invalid channel %i" % ch
		_uart = UartAdapter( self, ch )
		if len(kwargs)>0:
			_uart.init( **kwargs )
		return _uart

	def enable_irq( self, which ):
		# See xxx_INT constants 
		
		if (which & (CST_INT | RTS_INT | XOFF_INT | SLEEP_INT) )>0:
			# IER[7:4] can only be modified if EFR[4] is set, that is, EFR[4] is a write enable. 
			# Re-enabling IER[1] will not cause a new interrupt if the THR is below the threshold.
			raise NotImplementedError( 'IER[7:4] not implemented!' )

		_ier = self.bus_wrapper.read_reg( REG_IER, ch=0 )
		_ier = _ier | which
		self.bus_wrapper.write_reg( REG_IER, _ier, ch=0 )

	def rxtx_level( self, rx_level, tx_level ):
		# rx_level : 8, 16, 56, 60 characters 
		# tx_level : 8, 16, 32, 56 spaces
		assert rx_level in FCR_RX_LEVEL.keys(), "rx_level must be in %s" % FCR_RX_LEVEL.keys()
		assert tx_level in FCR_TX_LEVEL.keys(), "tx_level must be in %s" % FCR_TX_LEVEL.keys()

		rx_bits = FCR_RX_LEVEL[rx_level]
		tx_bits = FCR_TX_LEVEL[tx_level]
		
		# Activate write enable for FCR[4:5]
		old_efr = self.bus_wrapper.read_reg( REG_EFR, ch=0)
		_efr = old_efr | 0b00010000
		self.bus_wrapper.write_reg( REG_EFR, _efr, ch=0)

		_fcr = FCR_INIT_VALUE | (rx_bits<<6) | (tx_bits<<4)
		self.bus_wrapper.write_reg( REG_FCR, _fcr, ch=0) # with Clear TX FIFOs, Clear RX Fifo, Enable FiFo
		time.sleep_ms(1) # Reset requires minimum waiting of 2*Tclk

		# Restore previous configuration
		self.bus_wrapper.write_reg( REG_EFR, old_efr, ch=0)


	def line_level( self, rx_level=None, tx_level=None ):
		# Define the levels for line transmission (modem?). At least one of both parameter must be defines.
		# This function act on TLR (Trigger Level) instead of TCR (automatic Transmission Control).
		# Both feature cannot be used togheter! 
		#
		# TCR & TLR are accessible only when ERF[4] = 1 and MCR[2] = 1, that is, EFR[4] and MCR[2] are read/write enables.
		assert rx_level or tx_level, "At least rx_level or tx_level must be defined"

		if rx_level!=None:
			assert 4<=rx_level<=60, "RX level must be within 4-60 range"
			assert (rx_level%4)==0, "Level are step by 4!"
		if tx_level!=None:
			assert 4<=tx_level<=60, "TX level must be within 4-60 range"
			assert (tx_level%4)==0, "Level are step by 4!"
		if (rx_level!=None) and (tx_level!=None):
			assert tx_level > rx_level, "tx_level must be greater than rx_level!"

		# Set the 
		_tx_val = 0
		_rx_val = 0
		if tx_level!=None:
			_tx_val = tx_level//4
		if rx_level!=None:
			_rx_val = rx_level//4
	
		# Set LCR=0xBF to access EFR register
		_old_lcr = self.bus_wrapper.read_reg( REG_LCR, ch=0 ) # store transmission config (eg: 8n1)
		self.bus_wrapper.write_reg( REG_LCR, 0xBF, ch=0 )

		# Enable TCR & TLR register access
		_mcr = self.bus_wrapper.read_reg(REG_MCR, ch=0)
		_mcr = _mcr | 0b00000100
		self.bus_wrapper.write_reg(REG_MCR, _mcr, ch=0)

		# TCR must be cleared (to use TLR)
		self.bus_wrapper.write_reg(REG_TCR, 0x00, ch=0)

		# Set TLR trigger values
		_tlr = self.bus_wrapper.read_reg(REG_TLR, ch=0)
		_tlr = _tlr | (_rx_val<<4)
		_tlr = _tlr | _tx_val
		self.bus_wrapper.write_reg(REG_TLR, _tlr, ch=0)

		# Disable TCR & TLR register access
		_mcr = self.bus_wrapper.read_reg(REG_MCR, ch=0)
		_mcr = _mcr & 0b11111011
		self.bus_wrapper.write_reg(REG_MCR, _mcr, ch=0)

		self.bus_wrapper.write_reg( REG_LCR, 0xBF, ch=0 )

		# Close access to EFR & restore transmission config (eg:8n1)
		self.bus_wrapper.write_reg( REG_LCR, _old_lcr, ch=0 )


	def irq_source( self ):
		# Return a list of IRQs source ordered by priority 		
		_iir = self.bus_wrapper.read_reg( REG_IIR, ch=0 )
		if (_iir & 0b1) > 0: # No interrupt pending
			return None
		_iir = (_iir>>1) & 0b11111
		return _iir


# ============================================
#
#    SC16IS740, etc  Classes
#
# ============================================

class SC16IS740(SC16IS7XX):
	def __init__( self, **kwargs ):
		super().__init__( **kwargs )
		self._uart1 = None

	def uart( self, id, **kwargs ):
		assert id==1, "Only have ID 1 "
		if self._uart1 == None:
			self._uart1 = self.get_uart( owner=self, ch=id-1, **kwargs ) 
		return self._uart1


class SC16IS750(SC16IS740):
	def __init__( self, **kwargs ):
		super().__init__( **kwargs )
		self.pins = [ None, None, None, None, None, None, None, None ] # Refs to created Pin

	def pin( self, id, mode, **kwargs ):	
		assert 0<=id<=7, "Invalid Pin ID %s" % id
		if self.pins[id] != None:
			return self.pins[id]

		self.pins[id] = PinAdapter( owner=self, id=id )
		kwargs['mode']=mode
		self.pins[id].init( **kwargs )
		return self.pins[id]
