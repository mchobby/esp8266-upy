# Simple GPS module demonstration.
# Will wait for a fix and print a message every second with the current location
# and other details.
from machine import UART
import utime as time

import adafruit_gps

# Create a GPS module instance.
# uart = UART(1, baudrate=9600, timeout_chars=3000, pins=('P8','P2'))

# Pyboard (use timeout instead of timeout_chars)
uart = UART( 1, baudrate=9600, timeout=3000 ) # TX=X9, RX=X10


# Create a GPS module instance.
gps = adafruit_gps.GPS(uart)

# Initialize the GPS module by changing what data it sends and at what rate.
# These are NMEA extensions for PMTK_314_SET_NMEA_OUTPUT and
# PMTK_220_SET_NMEA_UPDATERATE but you can send anything from here to adjust
# the GPS module behavior:
#   https://cdn-shop.adafruit.com/datasheets/PMTK_A11.pdf

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn on just minimum info (RMC only, location):
#gps.send_command('PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Turn off everything:
#gps.send_command('PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
# Tuen on everything (not all of it is parsed!)
#gps.send_command('PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz) which is what you typically want.
gps.send_command('PMTK220,1000')
# Or decrease to once every two seconds by doubling the millisecond value.
# Be sure to also increase your UART timeout above!
#gps.send_command('PMTK220,2000')
# You can also speed up the rate, but don't go too fast or else you can lose
# data during parsing.  This would be twice a second (2hz, 500ms delay):
#gps.send_command('PMTK220,500')

# Main loop runs forever printing the location, etc. every second.
last_print = time.ticks_ms()
while True:
    # Make sure to call gps.update() every loop iteration and at least twice
    # as fast as data comes from the GPS unit (usually every second).
    # This returns a bool that's true if it parsed new data (you can ignore it
    # though if you don't care and instead look at the has_fix property).
    gps.update()
    # Every second print out current location details if there's a fix.
    current = time.ticks_ms()
    if time.ticks_diff(current, last_print) >= 1000:
        last_print = current

        if not gps.has_fix:
            # Try again if we don't have a fix yet.
            print('Waiting for fix...')
            continue
        # We have a fix! (gps.has_fix is true)
        # Print out details about the fix like location, date, etc.
        print('=' * 40)  # Print a separator line.
        print('Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}'.format(
            gps.timestamp_utc[1],   # Grab parts of the time from the
            gps.timestamp_utc[2],  # struct_time object that holds
            gps.timestamp_utc[0],  # the fix time.  Note you might
            gps.timestamp_utc[3],  # not get all data like year, day,
            gps.timestamp_utc[4],   # month!
            gps.timestamp_utc[5]))
        print('Latitude: {} degrees'.format(gps.latitude))
        print('Longitude: {} degrees'.format(gps.longitude))
        print('Fix quality: {}'.format(gps.fix_quality))
        # Some attributes beyond latitude, longitude and timestamp are optional
        # and might not be present.  Check if they're None before trying to use!
        if gps.satellites is not None:
            print('# satellites: {}'.format(gps.satellites))
        if gps.altitude_m is not None:
            print('Altitude: {} meters'.format(gps.altitude_m))
        if gps.track_angle_deg is not None:
            print('Speed: {} knots and {} km/h'.format(gps.speed_knots,gps.speed_knots*1.8513))
        if gps.track_angle_deg is not None:
            print('Track angle: {} degrees'.format(gps.track_angle_deg))
        if gps.horizontal_dilution is not None:
            print('Horizontal dilution: {}'.format(gps.horizontal_dilution))
        if gps.height_geoid is not None:
            print('Height geo ID: {} meters'.format(gps.height_geoid))
