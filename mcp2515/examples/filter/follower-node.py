# --- Follower node  ----------------------------
# The follower node waits the messages sent by the master node.
# 
# This script uses filter to intercept the message of interest.
# In this case, the traffic_light_AA01 messages.
#
from machine import SPI, Pin
from canio import Message, Match
from mcp2515 import MCP2515
import time, struct

spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False ) 
canbus = MCP2515( spi, cs, debug=False)


# Some 29bits Node ID for sending messages the can bus
traffic_light_AA01 = 0x100FAA01 # NodeID : Identifies the type of message/data
traffic_light_AA02 = 0x100FAA02 # NodeID : Identifies the type of message/data

level_crossing_BB01 = 0x100FBB01 

street_light_AA01   = 0x1A00AA01
street_light_AA02   = 0x1A00AA02



# Prepare the match (avoids multiple creation)
# extended is set to True because we are on 29bits
_match1 = Match( address=traffic_light_AA01, extended=True )


print('Listening on %s node...' % hex(_match1.address))
while True:
    with canbus.listen(matches=[_match1] ,timeout=1.0) as listener:
        # Process the received messages
        message_count = listener.in_waiting()
        # print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            # Display the remote node ID
            print("Message for ", hex(msg.id), "extended:", msg.extended)
            print("\tdata:", msg.data)
            # Decode the float value sent by the sensor node
            values = struct.unpack('B', msg.data ) # Always returns a typle
            print( "\tvalue:", values[0] )
            print("")

