"""
test_gir.py is a micropython example for Olimex MOD-RS485-ISO board + Girouette RS485.

Switch to Bridged Mode (data via I2C), set bus to 9600 baud and send ModBus request

MOD-RS485-ISO board : http://shop.mchobby.be/product.php?id_product=1414
MOD-RS485-ISO board : https://www.olimex.com/Products/Modules/Interface/MOD-RS485-ISO/open-source-hardware
GIROUETTE : https://shop.mchobby.be/product.php?id_product=2241

Remarks:
 * this is a RAW proof of concept.
   State of art coding is not used here, please be comprehensive!

"""
from machine import I2C
from rs485iso import RS485ISO, TX_ENABLED, RX_ENABLED, BRIDGE_MODE, UART_B9600
from time import sleep_ms

# Pyboard - I2C(2) - Y10=sda, Y9=scl
i2c = I2C(2)

rs485 = RS485ISO( i2c )

print( "Setting RX/TX control..." )
rs485.control = (TX_ENABLED | RX_ENABLED)
print( "Setting bridged mode..." )
# Data emitted to RS485 bus will be sent over I2C
rs485.mode = BRIDGE_MODE
print( "Setting baud..." )
rs485.baud_rate = UART_B9600

def dir_as_text( value ):
    if value==0:
        return 'North'
    if value==1:
        return 'Northeast by North'
    if value==2:
        return 'Northeast'
    if value==3:
        return 'Northeast by east'
    if value==4:
        return 'East'
    if value==5:
        return 'Southeast by east'
    if value==6:
        return 'Southeast'
    if value==7:
        return 'Southeast by south'
    if value==8:
        return 'South'
    if value==9:
        return 'Southwest by south'
    if value==10:
        return 'Southwest'
    if value==11:
        return 'Southwest by west'
    if value==12:
        return 'West'
    if value==13:
        return 'Northwest by west'
    if value==14:
        return 'Northwest'
    if value==15:
        return 'Northwest by north'
    return '???'

# Mod bus request to require Wind Direction data
# see https://wiki.dfrobot.com/RS485_Wind_Direction_Transmitter_SKU_SEN0482#target_2
def request():
    global rs485
    request = [0x02,0x03,0x00,0x00,0x00,0x01,0x84,0x39]
    winddir_data = bytearray( request )
    rs485.send( winddir_data )
    # Wait the data to be sent
    sleep_ms( 10 )
    # flush the sended data echoed into the  receive buffer
    buf1 = bytearray( 1 )
    while len(request)>0:
       rs485.read( buf1 )
       if buf1[0] in request:
           request.remove( buf1[0] )

def read_response():
    """ Read response data from RS485, extract direction, convert it to text.
        finally print the direction text. """
    global rs485
    # Response in 7 bytes
    buf = bytearray( 7 )
    rs485.read( buf )
    #print( 'Buffer: ', hex(buf[0]), hex(buf[1]), hex(buf[2]), hex(buf[3]), hex(buf[4]), hex(buf[5]), hex(buf[6]) )

    # Decode the response
    # 0 & 1 are the slave addr + function code
    if not(  (buf[0]==0x02) and (buf[1]==0x03) ):
        raise Exception( 'Invalid Slave/function' )
    if buf[2] != 0x02:
        raise Exception( 'Invalid response length' )
    # bytes 3 & 4 are the data. With value from 0 to 15, we do only need the
    # lower byte value (higher byte will always be 0)

    # print the direction label
    label = dir_as_text( buf[4] )
    print( 'Direction:', label )

    # bytes 5 & 6 are CRC (not checked here)

def read_dir():
    """ Send a request over RS485 THEN acquire & decode the RS485 response """
    request()
    sleep_ms( 100 ) # give sometime for the buffer to get data
    try:
        read_response()
    except Exception as err:
        print( 'Error decoding response' )
        print( '[ERROR]', err )
    sleep_ms( 1000 )

# Main routine
while True:
    read_dir()

print( 'That s all Folks' )
