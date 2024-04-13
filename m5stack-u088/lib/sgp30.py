"""
sgp30.py : MicroPython driver for M5Stack U088, eCO2, TVOC on SGP30 I2C sensor.

* Author(s):
   11 Apr 2024: Meurisse D. (shop.mchobby.be) - port to MicroPython
                Based on Adafruit CircuitPython https://github.com/adafruit/Adafruit_CircuitPython_SGP30.git
   ?? ??? 2017: CircuitPython source from ladyada for Adafruit Industries
                MIT license,
                Source almost not modified.
"""

__version__ = "0.0.1.0"
__repo__ = "https://github.com/mchobby/esp8266-upy/tree/master/m5stack-u088"

from micropython import const
import time
import struct

_SGP30_FEATURESETS = (0x0020, 0x0022)

_SGP30_CRC8_POLYNOMIAL = const(0x31)
_SGP30_CRC8_INIT = const(0xFF)
_SGP30_WORD_LEN = const(2)

class SGP30:
    def __init__(self, i2c, address = 0x58):
        """Initialize the sensor, get the serial # and verify that we found a proper SGP30"""
        self.i2c = i2c
        self.addr = address

        # get unique serial, its 48 bits so we store in an array
        self.serial = self._i2c_read_words_from_cmd([0x36, 0x82], 0.01, 3)
        # get featureset
        featureset = self._i2c_read_words_from_cmd([0x20, 0x2F], 0.01, 1)
        if featureset[0] not in _SGP30_FEATURESETS:
            raise RuntimeError("SGP30 Not detected")
        self.iaq_init()

    def _generate_crc(self, data: bytearray):
        """8-bit CRC algorithm for checking data"""
        crc = _SGP30_CRC8_INIT
        # calculates 8-Bit checksum with given polynomial
        for byte in data:
            crc ^= byte
            for _ in range(8):
                if crc & 0x80:
                    crc = (crc << 1) ^ _SGP30_CRC8_POLYNOMIAL
                else:
                    crc <<= 1
        return crc & 0xFF

    def _i2c_read_words_from_cmd( self, command, delay, reply_size ):
        """Run an SGP command query, get a reply and CRC results if necessary"""
        self.i2c.writeto( self.addr, bytes(command))
        time.sleep(delay)
        if not reply_size:
            return None
        crc_result = bytearray(reply_size * (_SGP30_WORD_LEN + 1))
        self.i2c.readfrom_into( self.addr, crc_result )
        # print("\tRaw Read: ", crc_result)
        result = []
        for i in range(reply_size):
            word = [crc_result[3 * i], crc_result[3 * i + 1]]
            crc = crc_result[3 * i + 2]
            if self._generate_crc(word) != crc:
                raise RuntimeError("CRC Error")
            result.append(word[0] << 8 | word[1])
        # print("\tOK Data: ", [hex(i) for i in result])
        return result

    def _run_profile(self, profile):
        """Run an SGP 'profile' which is a named command set """
        # command set is made of Tuple( name:str, command:List[int], signals/reply_size:int, delay:float] )"""
        name, command, signals, delay = profile
        return self._i2c_read_words_from_cmd(command, delay, signals)

    def iaq_init(self) -> List[int]:
        """Initialize the IAQ algorithm"""
        self._run_profile( ("iaq_init", [0x20, 0x03], 0, 0.01) ) # name, command, signals=reply_size, delay

    def iaq_measure(self):
        """Measure the eCO2 and TVOC"""
        return self._run_profile(("iaq_measure", [0x20, 0x08], 2, 0.05)) # # name, command, signals=reply_size, delay

    def get_iaq_baseline(self):
        """Retreive the IAQ algorithm baseline for eCO2 and TVOC"""
        return self._run_profile(("iaq_get_baseline", [0x20, 0x15], 2, 0.01)) # name, command, signals, delay

    def set_iaq_baseline(  self, eCO2, TVOC ):
        """Set the previously recorded IAQ algorithm baseline for eCO2 and TVOC"""
        if eCO2 == 0 and TVOC == 0:
            raise RuntimeError("Invalid baseline")
        buffer = []
        for value in [TVOC, eCO2]:
            arr = [value >> 8, value & 0xFF]
            arr.append(self._generate_crc(arr))
            buffer += arr
        self._run_profile(("iaq_set_baseline", [0x20, 0x1E] + buffer, 0, 0.01))

    def set_iaq_humidity(self, gramsPM3 ):
        """Set the humidity in g/m3 for eCO2 and TVOC compensation algorithm"""
        tmp = int(gramsPM3 * 256)
        buffer = []
        for value in [tmp]:
            arr = [value >> 8, value & 0xFF]
            arr.append(self._generate_crc(arr))
            buffer += arr
        self._run_profile(("iaq_set_humidity", [0x20, 0x61] + buffer, 0, 0.01))

    def set_iaq_relative_humidity(self, celsius: float, relative_humidity: float):
        """
        Set the humidity in g/m3 for eCo2 and TVOC compensation algorithm.
        The absolute humidity is calculated from the temperature (Celsius)
        and relative humidity (as a percentage).
        """
        numerator = ((relative_humidity / 100) * 6.112) * exp(
            (17.62 * celsius) / (243.12 + celsius)
        )
        denominator = 273.15 + celsius

        humidity_grams_pm3 = 216.7 * (numerator / denominator)
        self.set_iaq_humidity(humidity_grams_pm3)

    def raw_measure(self):
        """Measure H2 and Ethanol (Raw Signals in ticks)"""
        return self._run_profile(("raw_measure", [0x20, 0x50], 2, 0.025)) # name, command, signals=replay_size, delay

    @property
    def TVOC(self):
        """Total Volatile Organic Compound in parts per billion."""
        return self.iaq_measure()[1]

    @property
    def baseline_TVOC(self):
        """Total Volatile Organic Compound baseline value"""
        return self.get_iaq_baseline()[1]

    @property
    def eCO2(self):
        """Carbon Dioxide Equivalent in parts per million"""
        return self.iaq_measure()[0]

    @property
    def baseline_eCO2(self):
        """Carbon Dioxide Equivalent baseline value"""
        return self.get_iaq_baseline()[0]

    @property
    def Ethanol(self):
        """Ethanol Raw Signal in ticks"""
        return self.raw_measure()[1]

    @property
    def H2(self):
        """H2 Raw Signal in ticks"""
        return self.raw_measure()[0]
