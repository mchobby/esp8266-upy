""" Based on the Radomir Dopieralski works.
    micropython-pca9685 available at https://bitbucket.org/thesheep/micropython-pca9685/src/c8dec836f7a4?at=default

    July 11, 2016 - I2C fixes - DMeurisse (shop.mchobby.be)
	Sept 13, 2019 - compatible against machine.I2C (mpy 1.10)"""
import ustruct
import time


class PCA9685:
    def __init__(self, i2c, address=0x40):
        self.i2c = i2c
        self.address = address
        self.reset()

    def _write(self, address, value):
        #self.i2c.mem_write(bytearray([value]), self.address, address )
        self.i2c.writeto_mem( self.address, address, bytearray([value]) )

    def _read(self, address):
        #return self.i2c.mem_read(1, self.address, address)[0]
        return self.i2c.readfrom_mem(self.address, address, 1)[0]

    def reset(self):
        self._write(0x00, 0x00) # Mode1

    def freq(self, freq=None):
        if freq is None:
            return int(25000000.0 / 4096 / (self._read(0xfe) - 0.5))
        prescale = int(25000000.0 / 4096.0 / freq + 0.5)
        old_mode = self._read(0x00) # Mode 1
        self._write(0x00, (old_mode & 0x7F) | 0x10) # Mode 1, sleep
        self._write(0xfe, prescale) # Prescale
        self._write(0x00, old_mode) # Mode 1
        time.sleep_us(5)
        self._write(0x00, old_mode | 0xa1) # Mode 1, autoincrement on

    def pwm(self, index, on=None, off=None):
        if on is None or off is None:
            data = self.i2c.mem_read(self.address, 0x06 + 4 * index, 4)
            return ustruct.unpack('<HH', data)
        data = ustruct.pack('<HH', on, off)
        #self.i2c.mem_write(data, self.address, 0x06 + 4 * index)
        self.i2c.writeto_mem( self.address, 0x06 + 4 * index, data )

    def duty(self, index, value=None, invert=False):
        if value is None:
            pwm = self.pwm(index)
            if pwm == (0, 4096):
                value = 0
            elif pwm == (4096, 0):
                value = 4095
            value = pwm[1]
            if invert:
                value = 4095 - value
            return
        if not 0 <= value <= 4095:
            return ValueError("Out of range")
        if invert:
            value = 4095 - value
        if value == 0:
            self.pwm(index, 0, 4096)
        elif value == 4095:
            self.pwm(index, 4096, 0)
        else:
            self.pwm(index, 0, value)
