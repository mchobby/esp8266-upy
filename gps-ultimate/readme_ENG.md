[Ce fichier existe également en FRANCAIS](readme.md)

# Using GPS to get latitude and longitude
The GPS module helps you to get your localisation on the earth. It can also be used to get the time.

![GPS Ultimate](docs/_static/gps-ultimate.jpg)

Note:
1. The GPS sends NMEA even with NO GPS FIX. The NMEA stream just indicates that the fix is not available.
2. The Fix signal is available as breakout pin. The signal on this pin is the same as the FIX LED.
3. The FIX LED:
   * Flash every second when the GPS FIX is not available.
   * Flash once every 10 seconds when the GPS has a FIX.

# Credit

This library is based on Adafruit_CircuitPython_GPS available at:
https://github.com/adafruit/Adafruit_CircuitPython_GPS

Content also based on the work of "alexmrqt" available at:
https://github.com/alexmrqt/micropython-gps/commits/master

Distributed under the original MIT License.

# Library

The library must be copied on the MicroPython board before using the examples.

On a WiFi capable plateform:

```
>>> import mip
>>> mip.install("github:mchobby/esp8266-upy/gps-ultimate")
```

Or via the mpremote utility :

```
mpremote mip install github:mchobby/esp8266-upy/gps-ultimate
```

# Wiring

![GPS Ultimate to Pyboard](docs/_static/gps-ultimate-pyboard.jpg)

* The X9 & X10 are the pin of __UART(1)__.

# Testing

## Raw reading of NMEA streams
The `testraw.py` sample just send configuration string to the GPS module then parse incoming bytes on the serial line.

When the line feed is received, the `process_buffer()` is called. This function only prints the buffer content to the REPL output.

```
>>> import testraw
bytearray(b'L\x89\xa2\x82\x92br\xb100424.0478,E,1,07,1.19,94.7,M,47.4,M,,*52\r\n')
bytearray(b'$GPRMC,201225.,A,5041.4402,N,00424.0478,E,0.00,295.03,290719,,,A*6A\r\n')
bytearray(b'$PMTK001,314,3*36\r\n')
bytearray(b'$PMTK001,220,3*30\r\n')
bytearray(b'$GPGGA,201225.200,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*50\r\n')
bytearray(b'$GPRMC,201225.200,A,5041.4402,N,00424.0478,E,0.01,340.31,290719,,,A*61\r\n')
bytearray(b'$GPGGA,201225.400,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*56\r\n')
bytearray(b'$GPRMC,201225.400,A,5041.4402,N,00424.0478,E,0.01,356.93,290719,,,A*68\r\n')
bytearray(b'$GPGGA,201225.600,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*54\r\n')
bytearray(b'$GPRMC,201225.600,A,5041.4402,N,00424.0478,E,0.01,336.34,290719,,,A*61\r\n')
bytearray(b'$GPGGA,201225.800,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*5A\r\n')
bytearray(b'$GPRMC,201225.800,A,5041.4402,N,00424.0478,E,0.01,333.71,290719,,,A*6B\r\n')
bytearray(b'$GPGGA,201226.000,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*51\r\n')
bytearray(b'$GPRMC,201226.000,A,5041.4402,N,00424.0478,E,0.01,331.63,290719,,,A*61\r\n')
bytearray(b'$GPGGA,201226.200,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*53\r\n')
bytearray(b'$GPRMC,201226.200,A,5041.4402,N,00424.0478,E,0.00,343.31,290719,,,A*60\r\n')
bytearray(b'$GPGGA,201226.400,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*55\r\n')
bytearray(b'$GPRMC,201226.400,A,5041.4402,N,00424.0478,E,0.00,299.06,290719,,,A*64\r\n')
bytearray(b'$GPGGA,201226.600,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*57\r\n')
bytearray(b'$GPRMC,201226.600,A,5041.4402,N,00424.0478,E,0.01,290.00,290719,,,A*68\r\n')
bytearray(b'$GPGGA,201226.800,5041.4402,N,00424.0478,E,1,07,1.20,94.7,M,47.4,M,,*53\r\n')
bytearray(b'$GPRMC,201226.800,A,5041.4402,N,00424.0478,E,0.01,359.98,290719,,,A*63\r\n')
bytearray(b'$GPGGA,201227.000,5041.4402,N,00424.0478,E,1,07,1.20,94.7,M,47.4,M,,*5A\r\n')
bytearray(b'$GPRMC,201227.000,A,5041.4402,N,00424.0478,E,0.01,30.54,290719,,,A*56\r\n')
bytearray(b'$GPGGA,201227.200,5041.4402,N,00424.0478,E,1,07,1.20,94.7,M,47.4,M,,*58\r\n')
bytearray(b'$GPRMC,201227.200,A,5041.4402,N,00424.0478,E,0.01,29.49,290719,,,A*50\r\n')
bytearray(b'$GPGGA,201227.400,5041.4402,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*54\r\n')
bytearray(b'$GPRMC,201227.400,A,5041.4402,N,00424.0478,E,0.00,357.90,290719,,,A*69\r\n')
bytearray(b'$GPGGA,201227.600,5041.4403,N,00424.0478,E,1,07,1.19,94.7,M,47.4,M,,*57\r\n')
bytearray(b'$GPRMC,201227.600,A,5041.4403,N,00424.0478,E,0.00,359.85,290719,,,A*60\r\n')
```
Notes:
* The first line appears wierd because the data has been collected in the middle of the stream
* The \r\n (carriage return, linefeed) in included in the buffer.

## Test the GPS library

See `examples/minimaltest.py` rely on `adafruit_gps` library to perform the parsing and printing GPS location. That demonstration script shows a minimum of information on the output.

Please see the `simpletest.py` for the whole GPS information set displays.

Important: the uart must be created at 9600 baud with __timeout set to 3000ms__. Without proper timeout setting, the library will fail to work properly

``` python
from machine import UART
import utime as time

import adafruit_gps

# Pyboard (TX=X9, RX=X10)
uart = UART( 1, baudrate=9600, timeout=3000)

# Create a GPS instance
gps = adafruit_gps.GPS(uart)

# Turn on the basic GGA and RMC info
gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz)
gps.send_command('PMTK220,1000')

# Main loop runs
last_print = time.ticks_ms()
while True:
    gps.update()
    # Every second print
    current = time.ticks_ms()
    if time.ticks_diff(current, last_print) >= 1000:
        last_print = current

        if not gps.has_fix:
            print('Waiting for fix...')
            continue

        print('=' * 40)  
        print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
            gps.timestamp_utc[1],  
            gps.timestamp_utc[2],
            gps.timestamp_utc[0],
            gps.timestamp_utc[3],
            gps.timestamp_utc[4],
            gps.timestamp_utc[5]))
        print('Latitude: {} degrees'.format(gps.latitude))
        print('Longitude: {} degrees'.format(gps.longitude))
        if gps.satellites is not None:
            print('# satellites: {}'.format(gps.satellites))
        if gps.track_angle_deg is not None:
            print('Speed: {} km/h'.format(gps.speed_knots*1.8513))
```

The location is obtain with

``` python

    print('Latitude: {0:.6f} degrees'.format(gps.latitude))
    print('Longitude: {0:.6f} degrees'.format(gps.longitude))
```

Note: Sending multiple PMTK314 packets with `gps.send_command()` will not work unless there is a substantial amount of time in-between each time `gps.send_command()` is called. A `time.sleep()` of 1 second or more should fix this.

# Ressources
## About NMEA Data

This GPS module uses the NMEA 0183 protocol.

This data is formatted by the GPS in one of two ways.

The first of these is GGA. GGA has more or less everything you need.

Here's an explanation of GGA:
```

                                                        11
           1         2       3 4        5 6 7  8   9  10 |  12 13  14   15
           |         |       | |        | | |  |   |   | |   | |   |    |
    $--GGA,hhmmss.ss,llll.ll,a,yyyyy.yy,a,x,xx,x.x,x.x,M,x.x,M,x.x,xxxx*hh
```

1. Time (UTC)
2. Latitude
3. N or S (North or South)
4. Longitude
5. E or W (East or West)
6. GPS Quality Indicator,

   * 0 - fix not available,
   * 1 - GPS fix,
   * 2 - Differential GPS fix

7. Number of satellites in view, 00 - 12
8. Horizontal Dilution of precision
9. Antenna Altitude above/below mean-sea-level (geoid)
10. Units of antenna altitude, meters
11. Geoidal separation, the difference between the WGS-84 earth ellipsoid and mean-sea-level (geoid), "-" means mean-sea-level below ellipsoid
12. Units of geoidal separation, meters
13. Age of differential GPS data, time in seconds since last SC104 type 1 or 9 update, null field when DGPS is not used
14. Differential reference station ID, 0000-1023
15. Checksum

The second of these is RMC. RMC is Recommended Minimum Navigation Information.

Here's an explanation of RMC:
```
                                                               12
           1         2 3       4 5        6 7   8   9   10   11|
           |         | |       | |        | |   |   |    |   | |
    $--RMC,hhmmss.ss,A,llll.ll,a,yyyyy.yy,a,x.x,x.x,xxxx,x.x,a*hh
```

1. Time (UTC)
2. Status, V = Navigation receiver warning
3. Latitude
4. N or S
5. Longitude
6. E or W
7. Speed over ground, knots
8. Track made good, degrees true
9. Date, ddmmyy
10. Magnetic Variation, degrees
11. E or W
12. Checksum

The content of lines can be compared decode with the following documentations:
* [NMEA 0183 on wikipedia](https://fr.wikipedia.org/wiki/NMEA_0183)
* [Adafruit_GPS GitHub](https://github.com/adafruit/Adafruit_GPS)
* [NMEA0183 (pdf) @ tronico](https://www.tronico.fi/OH6NT/docs/NMEA0183.pdf)
* [NMEA sentences @ GpsInformation.org](https://www.gpsinformation.org/dale/nmea.htm)

# Shopping list
* [Adafruit GPS Ultimate (ADA-746)](https://shop.mchobby.be/product.php?id_product=62) @ MCHobby
* [Adafruit GPS Ultimate (ADA-746)](https://www.adafruit.com/product/746) @ Adafruit Industries
