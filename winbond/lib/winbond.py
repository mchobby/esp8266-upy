""" Implementation to interact with Winbond W25Q Flash with software reset.

Works with polarity=1, phase=1 (from BrainElectronics) or the default
polarity=0, phase=0 mostly used with sensors and others.

See https://github.com/mchobby/esp8266-upy/tree/master/winbond

History
	2024 apr 10, domeu, fix syntax error line 176 or original code
						_await gets extra parameter (timeout in sec) to allow formatting
						Reducing file size (strip comments and types)
						Plateform Agnostic creation


Credit to brainelectronics
  https://github.com/brainelectronics/micropython-winbond
Credits & kudos to crizeo
  Taken from https://forum.micropython.org/viewtopic.php?f=16&t=3899
"""

__version__ = '0.0.1'

from micropython import const
import time
from machine import SPI, Pin


class W25QFlash(object):
	"""W25QFlash implementation"""
	SECTOR_SIZE = const(4096)
	BLOCK_SIZE = const(512)
	PAGE_SIZE = const(256)

	def __init__(self, spi, cs, software_reset = True):
		self._manufacturer = 0x0
		self._mem_type = 0
		self._device_type = 0x0
		self._capacity = 0

		self.cs = cs
		self.spi = spi
		self._busy = False

		if software_reset:
			self.reset()

		# buffer for writing single blocks
		self._cache = bytearray(self.SECTOR_SIZE)

		# calc number of bytes (and makes sure the chip is detected and supported)
		self.identify()

		# address length (default: 3 bytes, 32MB+: 4)
		self._ADR_LEN = 3 if (len(bin(self._capacity - 1)) - 2) <= 24 else 4

		# setup address mode:
		if self._ADR_LEN == 4:
			if not self._read_status_reg(nr=16):  # not in 4-byte mode
				self._await()
				self.cs(0)
				self.spi.write(b'\xB7')  # 'Enter 4-Byte Address Mode'
				self.cs(1)

	@property
	def capacity(self):
		""" Get the storage capacity in bytes """
		return self._capacity

	@property
	def device(self):
		""" Get the flash device type """
		return self._device_type

	@property
	def manufacturer(self):
		# JEDEC manufacturer ID of the flash
		return self._manufacturer

	@property
	def mem_type(self):
		# Get the memory type of the flash (int)
		return self._mem_type

	def reset(self):
		# Reset the Winbond flash if the device has no hardware reset pin.
		# see original description @ https://github.com/brainelectronics/micropython-winbond
		if self._busy:
			self._await()
		self._busy = True
		self.cs(0)
		self.spi.write(b'\x66')  # 'Enable Reset' command
		self.cs(1)
		self.cs(0)
		self.spi.write(b'\x99')  # 'Reset' command
		self.cs(1)
		time.sleep_us(30)
		self._busy = False

	def identify(self):
		# Identify the Winbond chip.
		#  Determine the manufacturer and device ID and raises an error if the device is not detected or not supported.
		#  The capacity variable is set to the number of blocks (calculated based on the detected chip).
		self._await()
		self.cs(0)
		self.spi.write(b'\x9F')  # 'Read JEDEC ID' command

		# manufacturer id, memory type id, capacity id
		mf, mem_type, cap = self.spi.read(3, 0x00)
		self.cs(1)

		self._capacity = int(2**cap)

		if not (mf and mem_type and cap):  # something is 0x00
			raise OSError("device not responding, check wiring. ({}, {}, {})".
						  format(hex(mf), hex(mem_type), hex(cap)))
		if mf != 0xEF or mem_type not in [0x40, 0x60, 0x70]:
			# Winbond manufacturer, Q25 series memory (tested 0x40 only)
			print(f"Warning manufacturer ({hex(mf)}) or memory type",f"({hex(mem_type)}) not tested.")

		self._manufacturer = mf
		self._mem_type = mem_type
		self._device_type = mem_type << 8 | cap

	def get_size(self):
		# Get the flash chip size in bytes.
		return self._capacity

	def format(self, max_sec=20):
		""" Format the Winbond flash chip by resetting all memory to 0xFF. """
		# This may takes a lot of time Up to a minute for 128 MB chip.
		# Important: Run "os.VfsFat.mkfs(flash)" to make the flash an accessible
		# file system. As always, you will then need to
		# run os.mount(flash, '/MyFlashDir')" then to mount the flash
		self._wren()
		self._await()
		self.cs(0)
		self.spi.write(b'\xC7')  # 'Chip Erase' command
		self.cs(1)
		self._await(max_sec)  # wait for the chip to finish formatting with specific time

	def _read_status_reg(self, nr):
		reg, bit = divmod(nr, 8)
		self.cs(0)
		# 'Read Status Register-...' (1, 2, 3) command
		self.spi.write((b'\x05', b'\x35', b'\x15')[reg])
		stat = 2**bit & self.spi.read(1, 0xFF)[0]
		self.cs(1)

		return stat

	def _await(self, max_sec=2):
		# Wait for device not to be busy ()
		max_sec *= 10 # 20 * 100ms = 2 sec
		self._busy = True
		self.cs(0)
		self.spi.write(b'\x05')  # 'Read Status Register-1' command

		# last bit (1) is BUSY bit in stat. reg. byte (0 = not busy, 1 = busy)
		trials = 0
		while 0x1 & self.spi.read(1, 0xFF)[0]:
			if trials > max_sec:
				raise Exception("Device keeps busy, aborting.")
			time.sleep(0.1)
			trials += 1
		self.cs(1)
		self._busy = False

	def _sector_erase(self, addr):
		# Resets all memory within the specified sector (4kB) to 0xFF
		self._wren()
		self._await()
		self.cs(0)
		self.spi.write(b'\x20')  # 'Sector Erase' command
		self.spi.write(addr.to_bytes(self._ADR_LEN, 'big'))
		self.cs(1)

	def _read(self, buf, addr):
		# Read the length of the buffer bytes from the chip.
		# The buffer length has to be a multiple of self.SECTOR_SIZE (or less).
		assert addr + len(buf) <= self._capacity, "memory not addressable at %s with range %d (max.: %s)" % (hex(addr), len(buf), hex(self._capacity - 1))

		self._await()
		self.cs(0)
		# 'Fast Read' (0x03 = default), 0x0C for 4-byte mode command
		self.spi.write(b'\x0C' if self._ADR_LEN == 4 else b'\x0B')
		self.spi.write(addr.to_bytes(self._ADR_LEN, 'big'))
		self.spi.write(b'\xFF')  # dummy byte
		self.spi.readinto(buf, 0xFF)
		self.cs(1)

	def _wren(self):
		# Set the Write Enable Latch (WEL) bit in the status register
		self._await()
		self.cs(0)
		self.spi.write(b'\x06')  # 'Write Enable' command
		self.cs(1)

	def _write(self, buf, addr ):
		# Write the data of the given buffer to the address location
		# See details @
		assert len(buf) % self.PAGE_SIZE == 0, "invalid buffer length: {}".format(len(buf))
		assert not addr & 0xf, "address ({}) not at page start".format(addr)
		assert addr + len(buf) <= self._capacity, ("memory not addressable at {} with range {} (max.: {})".format(hex(addr), len(buf), hex(self._capacity - 1)))

		for i in range(0, len(buf), self.PAGE_SIZE):
			self._wren()
			self._await()
			self.cs(0)
			self.spi.write(b'\x02')  # 'Page Program' command
			self.spi.write(addr.to_bytes(self._ADR_LEN, 'big'))
			self.spi.write(buf[i:i + self.PAGE_SIZE])
			addr += self.PAGE_SIZE
			self.cs(1)

	def _writeblock(self, blocknum, buf): # list
		# Write a data block.
		# see details @ https://github.com/brainelectronics/micropython-winbond
		assert len(buf) == self.BLOCK_SIZE, "invalid block length: {}".format(len(buf))

		sector_nr = blocknum // 8
		sector_addr = sector_nr * self.SECTOR_SIZE
		# index of first byte of page in sector (multiple of self.PAGE_SIZE)
		index = (blocknum << 9) & 0xfff

		self._read(buf=self._cache, addr=sector_addr)
		self._cache[index:index + self.BLOCK_SIZE] = buf  # apply changes
		self._sector_erase(addr=sector_addr)
		# addr is multiple of self.SECTOR_SIZE, so last byte is zero
		self._write(buf=self._cache, addr=sector_addr)

	def readblocks(self, blocknum, buf): # buf: list
		# Read a data block. The length has to be a multiple of self.BLOCK_SIZE
		assert len(buf) % self.BLOCK_SIZE == 0, 'invalid buffer length: {}'.format(len(buf))

		buf_len = len(buf)
		if buf_len == self.BLOCK_SIZE:
			self._read(buf=buf, addr=blocknum << 9)
		else:
			offset = 0
			buf_mv = memoryview(buf)
			while offset < buf_len:
				self._read(buf=buf_mv[offset:offset + self.BLOCK_SIZE],
						   addr=blocknum << 9)
				offset += self.BLOCK_SIZE
				blocknum += 1

	def writeblocks(self, blocknum, buf):
		# Write a data block.The length has to be a multiple of self.BLOCK_SIZE
		buf_len = len(buf)
		if buf_len % self.BLOCK_SIZE != 0:
			# appends xFF dummy bytes
			buf += bytearray((self.BLOCK_SIZE - buf_len) * [255])

		if buf_len == self.BLOCK_SIZE:
			self._writeblock(blocknum=blocknum, buf=buf)
		else:
			offset = 0
			buf_mv = memoryview(buf)
			while offset < buf_len:
				self._writeblock(blocknum=blocknum,
								 buf=buf_mv[offset:offset + self.BLOCK_SIZE])
				offset += self.BLOCK_SIZE
				blocknum += 1
		# remove appended bytes
		buf = buf[:buf_len]

	def count(self):
		""" number of blocks available on the device """
		return int(self._capacity / self.BLOCK_SIZE)
