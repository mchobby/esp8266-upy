"""
test_reader.py is a micropython example for Olimex MOD-RS485-ISO board.

Switch to Bridged Mode (data via I2C), set bus to 9600 baud and read data

MOD-RS485-ISO board : http://shop.mchobby.be/product.php?id_product=1414
MOD-RS485-ISO board : https://www.olimex.com/Products/Modules/Interface/MOD-RS485-ISO/open-source-hardware

"""
from machine import I2C
from rs485iso import RS485ISO, RX_ENABLED, BRIDGE_MODE, UART_B9600
from time import sleep

# Pyboard - I2C(2) - Y10=sda, Y9=scl
i2c = I2C(2)

rs485 = RS485ISO( i2c )

print( "Setting RX control..." )
rs485.control = RX_ENABLED
print( "Setting bridged mode..." )
# Data received on RS485 bus will be forwarded over I2C
rs485.mode = BRIDGE_MODE
print( "Setting baud..." )
rs485.baud_rate = UART_B9600
print( "read 10 bytes buffer" )
buf10 = bytearray( 10 )
# Read full buffer
rs485.read( buf10 )
print( buf10 )

print("read 3 bytes only into the buffer")
# Read only 3 bytes into the buffer
# So only the 3 first bytes of the buffer are relevant (ignore the remaining)
rs485.read( buf10, max_read=3 )
print( buf10 )

print( 'That s all Folks' )
