# drivers.json - list of MicroPython drivers

The driver.json contains the list of drivers available in this repository.

It codifies the various information regarding the available drivers AND used to generate the root Readme on the repository.

For each entry in the list, you will have a dictionnary with the following entries:
* folder        : name of the sub-folder is the repository,
* components    : list of components managed by the driver (uppercase). Eg: ADS1115
* interfaces    : list of interface used in the divers like bus, special connector, etc. Must be listed in interfaces.json file. Eg: I2C, SPI, UART, NCD, UEXT, QWIIC.
* manufacturers : manufacturer of tested board/breakout with the driver. Must be listed in manufacturers.json. Eg: ADAFRUIT
* plateforms    : list of boards/plateforms for which wirings are available in the dedicated readme. Must be in plateforms.json. Eg: FEATHER-ESP8266
* ressources    : list of links
* descr         : dictionnary containing the "FR" and "ENG" entry for description

## ressource entry
Each entry is composed of
* label : label to display
* url   : corresponding link

# manufacturers.json - list of manufacturers

The manufacturers.json contains a dictionnary of manufacturer KEYs used in the drivers.

Each dictionnary entry contains the following data

* name : Name of the manufacturer.
* url  : Url of the manufacturer.

# plateforms.json - list of supported plateforms

The plateforms.json contains a dictionnary with the plateforms KEYs used in the drivers. Eg: PYBOARD, FEATHER-ESP8266, etc.

Each entry contains
* descr     : dictionnary containing the "FR" and "ENG" entry for description
* url		    : link to the target product

# interfaces.json - list of supported interfaces

The interfaces.json contains a dictionnary with the interface KEYs (Uppercase) used in the drivers. Eg: I2C, SPI, UEXT, NCD, etc.

Identifies communication interface used in the driver (like I2C, SPI) and/or hardware connection (NCD, UEXT, QWIIC). So combination of the both are possible.

* descr     : dictionnary containing the "FR" and "ENG" entry for description
