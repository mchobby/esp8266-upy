from machine import UART
import utime as time

import adafruit_gps

# Pyboard (TX=X9, RX=X10)
uart = UART( 1, baudrate=9600, timeout=3000)

# Create a GPS instance
gps = adafruit_gps.GPS(uart)

# Turn on the basic GGA and RMC info
gps.send_command( 'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')

# Set update rate to once a second (1hz)
gps.send_command( 'PMTK220,1000')

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
