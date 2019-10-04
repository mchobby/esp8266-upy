# commands to set the update rate (must be combine with position fix update)
PMTK_SET_NMEA_UPDATE_100_MILLIHERTZ  = "PMTK220,10000"  # Once every 10 seconds, 100 millihertz.
PMTK_SET_NMEA_UPDATE_200_MILLIHERTZ  = "$PMTK220,5000"  # Once every 5 seconds, 200 millihertz.
PMTK_SET_NMEA_UPDATE_1HZ  = "PMTK220,1000"              # 1 Hz
PMTK_SET_NMEA_UPDATE_2HZ  = "PMTK220,500"               # 2 Hz
PMTK_SET_NMEA_UPDATE_5HZ  = "PMTK220,200"               # 5 Hz
PMTK_SET_NMEA_UPDATE_10HZ = "PMTK220,100"               # 10 Hz

# Position fix update rate commands.
# Can't fix position faster than 5 times a second!
PMTK_API_SET_FIX_CTL_100_MILLIHERTZ  = "PMTK300,10000,0,0,0,0"  # Once every 10 seconds, 100 millihertz.
PMTK_API_SET_FIX_CTL_200_MILLIHERTZ  = "PMTK300,5000,0,0,0,0"   # Once every 5 seconds, 200 millihertz.
PMTK_API_SET_FIX_CTL_1HZ  = "PMTK300,1000,0,0,0,0"              # 1 Hz
PMTK_API_SET_FIX_CTL_5HZ  = "PMTK300,200,0,0,0,0"               # 5 Hz


PMTK_SET_BAUD_115200 = "PMTK251,115200"  # 115200 bps
PMTK_SET_BAUD_57600  = "PMTK251,57600"   # 57600 bps
PMTK_SET_BAUD_9600   = "PMTK251,9600"    # 9600 bps

# Type of NMEA sentence to output
PMTK_SET_NMEA_OUTPUT_GLLONLY = "PMTK314,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn on only the GPGLL sentence
PMTK_SET_NMEA_OUTPUT_RMCONLY = "PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn on only the GPRMC sentence
PMTK_SET_NMEA_OUTPUT_VTGONLY = "PMTK314,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn on only the GPVTG
PMTK_SET_NMEA_OUTPUT_GGAONLY = "PMTK314,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn on just the GPGGA
PMTK_SET_NMEA_OUTPUT_GSAONLY = "PMTK314,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn on just the GPGSA
PMTK_SET_NMEA_OUTPUT_GSVONLY = "PMTK314,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn on just the GPGSV
PMTK_SET_NMEA_OUTPUT_RMCGGA  = "PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn on GPRMC and GPGGA
PMTK_SET_NMEA_OUTPUT_ALLDATA = "PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn on ALL THE DATA
PMTK_SET_NMEA_OUTPUT_OFF     = "PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0"  # turn off output

# to generate your own sentences, check out the MTK command datasheet and use a checksum calculator
# such as the awesome http://www.hhhh.org/wiml/proj/nmeaxor.html

# Locus mode is an autonomous GPS PROCESS that acquire position and store in
# into internal GPS flash
PMTK_LOCUS_STARTLOG     = "PMTK185,0"     # Start logging data
PMTK_LOCUS_STOPLOG      = "PMTK185,1"     # Stop logging data
PMTK_LOCUS_STARTSTOPACK = "PMTK001,185,3" # Acknowledge the start or stop command
PMTK_LOCUS_QUERY_STATUS = "PMTK183"       # Query the logging status
PMTK_LOCUS_ERASE_FLASH  = "PMTK184,1"     # Erase the log flash data
LOCUS_OVERLAP  = 0                        # If flash is full, log will overwrite old data with new logs
LOCUS_FULLSTOP = 1                        # If flash is full, logging will stop

PMTK_ENABLE_SBAS = "PMTK313,1"   # Enable search for SBAS satellite (only works with 1Hz output rate)
PMTK_ENABLE_WAAS = "PMTK301,2"   # Use WAAS for DGPS correction data

PMTK_STANDBY         = "PMTK161,0"     # standby command & boot successful message
PMTK_STANDBY_SUCCESS = "PMTK001,161,3" # Not needed currently
PMTK_AWAKE           = "PMTK010,002"   # Wake up

PMTK_Q_RELEASE       = "PMTK605"       # ask for the release and version

PGCMD_ANTENNA   = "PGCMD,33,1"         # request for updates on antenna status
PGCMD_NOANTENNA = "PGCMD,33,0"         # don't show antenna status messages
