"""
test_check.py is a micropython example for Olimex MOD-RS485-ISO board.
It checks the MOD-RS485-ISO configuration.

MOD-RS485-ISO board : http://shop.mchobby.be/product.php?id_product=1414
MOD-RS485-ISO board : https://www.olimex.com/Products/Modules/Interface/MOD-RS485-ISO/open-source-hardware

"""

from machine import I2C
from rs485iso import *

# Pyboard - I2C(2) - Y10=sda, Y9=scl
i2c = I2C(2)

rs485 = RS485ISO( i2c )

print( "MOD-RS485-ISO" )
print( "======================================================" )

print( "  Device ID: %s" % hex(rs485.device_id) )
print( "  Firmware : %s" % hex(rs485.version) )

# The device can operate in two modes:
# - PASS MODE   - Signals on TX line pass straigth throw the device and are transmitted to RS-485 line. The same apply to the RX.
# - BRIDGE_MODE - TX and RX are disabled. Data can be send via I2C bus.
mode = rs485.mode
mode_text = 'PASS_MODE (data via uart)' if mode == PASS_MODE else 'BRIDGE_MODE (data via i2c)'
print( "  Mode     : %s - %s" % (hex(mode),mode_text ) )

# Direction is bitfield byte as follow made of the following constants
#   TX_ENABLED (bit 1), RX_ENABLED (bit 0)
#   values TX_DISABLED, RX_DISABLED can also be used
direction = rs485.control
direction_text = []
if (direction & TX_ENABLED) == TX_ENABLED:
	direction_text.append( 'TX enabled')
else:
	direction_text.append( 'TX disabled')

if (direction & RX_ENABLED) == RX_ENABLED:
	direction_text.append( 'RX enabled')
else:
	direction_text.append( 'RX disabled')
print( "  Direction: %s - %s" % ( hex(direction),', '.join(direction_text) ))

# Baud rate
BAUDRATE_AS_TEXT = {UART_B50      : "50",
				UART_B75      : "75",
				UART_B110     : "110",
				UART_B134     : "134",
				UART_B150     : "150",
				UART_B300     : "300",
				UART_B600     : "600",
				UART_B1200    : "1200",
				UART_B1800    : "1800",
				UART_B2400    : "2400",
				UART_B4800    : "4800",
				UART_B7200    : "7200",
				UART_B9600    : "9600",
				UART_B14400   : "14400",
				UART_B19200   : "19200",
				UART_B38400   : "38400",
				UART_B57600   : "57600",
				UART_B76800   : "76800",
				UART_B115200  : "115200",
				UART_B128000  : "128000",
				UART_B230400  : "230400",
				UART_B500000  : "500000",
				UART_B576000  : "576000",
				UART_B1000000 : "1000000" }

print( "  baudrate : %s" % ( BAUDRATE_AS_TEXT[rs485.baud_rate] ))
