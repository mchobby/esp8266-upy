""" DS3231 RTC driver

Datasheet:  https://datasheets.maximintegrated.com/en/ds/DS3231.pdf

Adapted from shaoziyang micropython driver (https://github.com/micropython-Chinese-Community/mpy-lib/)
Adapted from Pyboard driver for DS3231 precison real time clock (https://github.com/peterhinch/micropython-samples/)

Jan 1, 2021 : Th Monin, adapted from Pyboard Version for PYBStick
                        Alarm functions temporiraly removed (no useful test case)
                        Alarm constants for information
Apr 5, 2021 : Meurisse D., Make it plateform independant
                           preserve license

Copyright Th Monin 2021 Released under the MIT license.
"""

DS3231_I2C_ADDR   = 0x68
DS3231_REG_SEC    = 0x00
DS3231_REG_MIN    = 0x01
DS3231_REG_HOUR   = 0x02
DS3231_REG_WEEKDAY= 0x03
DS3231_REG_DAY    = 0x04
DS3231_REG_MONTH  = 0x05
DS3231_REG_YEAR   = 0x06

DS3231_REG_A1SEC  = 0x07
DS3231_REG_A1MIN  = 0x08
DS3231_REG_A1HOUR = 0x09
DS3231_REG_A1DAY  = 0x0A
DS3231_REG_A2MIN  = 0x0B
DS3231_REG_A2HOUR = 0x0C
DS3231_REG_A2DAY  = 0x0D
DS3231_REG_CTRL   = 0x0E
DS3231_REG_STA    = 0x0F
DS3231_REG_AGOFF  = 0x10
DS3231_REG_TEMP   = 0x11

# Day of Week
DOW_MONDAY        = 0
DOW_TUESDAY       = 1
DOW_WEDNESDAY     = 2
DOW_THURSDAY      = 3
DOW_FRIDAY        = 4
DOW_SATURDAY      = 5
DOW_SUNDAY        = 6

PER_DISABLE = 0
PER_MINUTE  = 1
PER_HOUR    = 2
PER_DAY     = 3
PER_WEEKDAY = 4
PER_MONTH   = 5


## --
## General functions

# BCD to decimal
def bcd2dec(bcd):
    return (((bcd & 0xf0) >> 4) * 10 + (bcd & 0x0f))

# Decimal to BCD
def dec2bcd(dec):
    tens, units = divmod(dec, 10)
    return (tens << 4) + units

## --
# Exception class
class DS3231Exception(Exception):
    pass

## --
# DS3231 main class
class DS3231():
    def __init__(self, i2c ):
        self.i2c = i2c
        self.write_reg(DS3231_REG_CTRL, 0x4C)

    def write_reg(self, reg, dat):
        self.i2c.mem_write(dat, DS3231_I2C_ADDR, reg, timeout=500)

    def read_reg(self, reg):
        return self.i2c.mem_read(1, DS3231_I2C_ADDR, reg)[0]

    def second(self, sec = None):
        if sec == None:
            return bcd2dec(self.read_reg(DS3231_REG_SEC))
        else:
            self.write_reg(DS3231_REG_SEC, dec2bcd(sec))

    def minute(self, min = None):
        if min == None:
            return bcd2dec(self.read_reg(DS3231_REG_MIN))
        else:
            self.write_reg(DS3231_REG_MIN, dec2bcd(min))

    def hour(self, hr = None):
        if hr == None:
            return bcd2dec(self.read_reg(DS3231_REG_HOUR))
        else:
            self.write_reg(DS3231_REG_HOUR, dec2bcd(hr))

    def weekday(self, wd = None):
        if wd == None:
            return bcd2dec(self.read_reg(DS3231_REG_WEEKDAY))
        else:
            self.write_reg(DS3231_REG_WEEKDAY, dec2bcd(wd))

    def day(self, dy = None):
        if dy == None:
            return bcd2dec(self.read_reg(DS3231_REG_DAY))
        else:
            self.write_reg(DS3231_REG_DAY, dec2bcd(dy))

    def month(self, mo = None):
        if mo == None:
            return bcd2dec(self.read_reg(DS3231_REG_MONTH))
        else:
            self.write_reg(DS3231_REG_MONTH, dec2bcd(mo))

    def year(self, yr = None):
        if yr == None:
            return bcd2dec(self.read_reg(DS3231_REG_YEAR)) + 2000
        else:
            self.write_reg(DS3231_REG_YEAR, dec2bcd(yr%100))

    def time(self, dat = None):
        if dat == None:
            return (self.hour(), self.minute(), self.second())
        else:
            self.hour(dat[0])
            self.minute(dat[1])
            self.second(dat[2])

    def date(self, prm = None):
        if prm == None:
            return (self.year(), self.month(), self.day())
        else:
            self.year(prm[0])
            self.month(prm[1])
            self.day(prm[2])

    def datetime(self, prm = None):
        if prm == None :
            return (self.date() + (self.weekday(),) + self.time() + (0,))
        else:
            self.date((prm[0], prm[1], prm[2]))
            self.weekday(prm[3])
            self.time((prm[4], prm[5], prm[6]))

    def temperature_raw(self):
        t_msb = self.read_reg(DS3231_REG_TEMP)
        t_lsb = self.read_reg(DS3231_REG_TEMP + 1)
        return t_msb, t_lsb

    def temperature(self):
        t_msb, t_lsb = self.temperature_raw()
        if (t_msb >> 7) == 1:
            return t_msb-256 - t_lsb/256
        else:
            return t_msb + t_lsb/256
