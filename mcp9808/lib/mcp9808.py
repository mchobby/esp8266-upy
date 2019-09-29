# The MIT License (MIT)
#
# 2019 Meurisse D for MCHobby.be - backport to MicroPython.
# Copyright (c) 2017 Scott Shawcroft for Adafruit Industries - original CircuitPython
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`mcp9808` - MCP9808 I2C Temperature Sensor
====================================================

MicroPython library to support MCP9808 high accuracy temperature sensor.

* Author(s): Meurisse D. for MCHobby.be - backport to MicroPython
* Author(s): Scott Shawcroft - original CircuiPython library

Implementation Notes
--------------------

**Hardware:**

* Adafruit `MCP9808 High Accuracy I2C Temperature Sensor Breakout
  <https://www.adafruit.com/products/1782>`_ (Product ID: 1782)

**Software and Dependencies:**

* MicroPython machin.I2C

**Notes:**

#.  Datasheet: http://www.adafruit.com/datasheets/MCP9808.pdf

"""

# Resolution settings
HALF_C = 0x0
QUARTER_C = 0x1
EIGHTH_C = 0x2
SIXTEENTH_C = 0x3

class MCP9808:
    """Interface to the MCP9808 temperature sensor."""

    # alert_lower_temperature_bound
    # alert_upper_temperature_bound
    # critical_temperature
    # temperature
    # temperature_resolution

    def __init__(self, i2c, address=0x18):
        self.i2c = i2c
        self.address = address

        # Verify the manufacturer and device ids to ensure we are talking to
        # what we expect.

        _data = bytes( [0x06] )
        self.i2c.writeto( self.address, _data )
        _data = self.i2c.readfrom( self.address, 2)

        ok = _data[1] == 0x54 and _data[0] == 0

        # Check device id.
        _data = bytes( [0x07] )
        self.i2c.writeto( self.address, _data )
        _data = self.i2c.readfrom( self.address, 2 )

        #if not ok or self.buf[1] != 0x04:
        if not ok or _data[0] != 0x04:
            raise ValueError("Unable to find MCP9808 at i2c address " + str(hex(address)))

    @property
    def temperature(self):
        """Temperature in celsius. Read-only."""
        _data = bytes( [0x05] )
        self.i2c.writeto(self.address, _data )
        _data = self.i2c.readfrom( self.address, 2 )
        # Clear flags from the value
        _data0 = _data[0] & 0x1f
        if _data0 & 0x10 == 0x10:
            _data0 = _data0 & 0x0f
            return (_data0 * 16 + _data[1] / 16.0) - 256
        return _data0 * 16 + _data[1] / 16.0
