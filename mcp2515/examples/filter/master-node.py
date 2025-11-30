# --- Master node  ----------------------------
# The master node is there to control a network of actuators (the follower)
# via the CAN bus.
#
# So, this script only send message/data to various NodeID.
#
# 
from machine import SPI,Pin,ADC, idle
from canio import Message
from mcp2515 import MCP2515
from time import sleep_ms
import struct

# MAster Node
master_id = 0x1fffffff # Highest Node ID

# Some 29bits Node ID for sending messages the can bus
traffic_light_AA01 = 0x100FAA01 # NodeID : Identifies the type of message/data
traffic_light_AA02 = 0x100FAA02 # NodeID : Identifies the type of message/data

level_crossing_BB01 = 0x100FBB01 

street_light_AA01   = 0x1A00AA01
street_light_AA02   = 0x1A00AA02

# Raspberry Pico
spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False ) 
canbus = MCP2515( spi, cs, debug=False)  
print('Master node ready...')


def send_message( value, node_id, node_label ):
    """ Send a value (0..255) to node_id. node_label is used to display debug messages """
    assert 0<=value<=255 
    print( "Send message to %s" % node_label )
    print("\tvalue :", value)
    data = struct.pack('B', value ) # Unsigned char (1 byte, 0..255 ) to binary
    message = Message(id=node_id, data=data, extended=True)
    send_success = canbus.send(message)
    if send_success:
        print("\tSent!")
    else:
        print("\tSend data failure")
    print( "" )


send_message(  67, traffic_light_AA01, "traffic_light_AA01")
send_message(   1,  street_light_AA02, "street_light_AA02")
send_message(  88,level_crossing_BB01, "level_crossing_BB01")
send_message( 129, traffic_light_AA02, "traffic_light_AA02")

