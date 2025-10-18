# Simple script using GPS timestamps as RTC time source
# The GPS timestamps are available without a fix and keep the track of
# time while there is powersource (ie coin cell battery)
#
# Tested on a Raspberry-Pi Pico
#
from machine import UART, RTC, Pin
from adafruit_gps import GPS
import time

rtc = RTC()
uart = UART(0, rx=Pin(1), tx=Pin(0), baudrate=9600, timeout=3000)

gps = GPS(uart)
gps.send_command('PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
gps.send_command('PMTK220,1000')

print("Set GPS as time source")
gps.update()
# we need a structure and we need the year to be filled
while (gps.timestamp_utc == None) or (gps.timestamp_utc[1]==0):
    print( 'Query GPS time...')
    time.sleep(0.5)
    gps.update()
datetime_from_gps = ( gps.timestamp_utc[0],  # tm_year
            gps.timestamp_utc[1],  # tm_mon (month)
            gps.timestamp_utc[2],  # tm_mday (day in the month)
            0, # day of week (don't care)
            gps.timestamp_utc[3]+1,  # tm_hour. UTC to Belgium Time => +1
            gps.timestamp_utc[4],   # tm_min
            gps.timestamp_utc[5],  # tm_sec
            0 ) # ms
print('  GPS Time', datetime_from_gps )
rtc.datetime( datetime_from_gps )


# Print current information
last_print = time.ticks_ms()
while True:

    gps.update()
    # Every second print out current time from GPS, RTC and time.localtime()
    current = time.ticks_ms()
    if time.ticks_diff(current, last_print) >= 1000:
        last_print = current
        print( "="*40 )
        # Time & date from GPS informations (UTC time)
        print('GPS FIX timestamp: {:02}/{:02}/{} {:02}:{:02}:{:02}'.format(
        # Grab parts of the time from the struct_time object that holds
        # the fix time.  Note you might not get all data like year, day,
        # month!
            gps.timestamp_utc[1],  # tm_mon (month)
            gps.timestamp_utc[2],  # tm_mday (day in the month)
            gps.timestamp_utc[0],  # tm_year
            gps.timestamp_utc[3],  # tm_hour
            gps.timestamp_utc[4],   # tm_min
            gps.timestamp_utc[5]))  # tm_sec

        #Time & date from internal RTC
        rtc_datetime = rtc.datetime()
        print('RTC timestamp: {:02}/{:02}/{} {:02}:{:02}:{:02}'.format(
            rtc_datetime[1], # tm_mon (month)
            rtc_datetime[2], # tm_mday (day in the month)
            rtc_datetime[0], # tm_year
            rtc_datetime[4], # tm_hour
            rtc_datetime[5], # tm_min
            rtc_datetime[6] )) # tm_sec

        #Time & date from time.localtime() function
        #  at format (2019, 10, 4, 13, 3, 17, 4, 277) y,m,d, HH,MM,SS,subS
        local_time = time.localtime()
        print("Local time: {:02}/{:02}/{} {:02}:{:02}:{:02}".format(
            local_time[1], # tm_mon (month)
            local_time[2], # tm_mday (day in the month)
            local_time[0], # tm_year
            local_time[3], # tm_hour
            local_time[4], # tm_min
            local_time[5] )) # tm_sec
