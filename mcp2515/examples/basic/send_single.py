#
# CanBus with MCP2515 - Send a single message and check transmission status
#
from machine import SPI,Pin
from canio import Message, RemoteTransmissionRequest
from mcp2515 import MCP2515
from time import sleep_ms

NODE_ID = 0x1234ABCD # NodeID : Identifies the type of message/data


# Raspberry Pico
spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False ) # Extra silent Pin for transceiver

canbus = MCP2515( spi, cs, debug=False)

print('Sending single message...')

# Sending a message (extended=True means that we use 29bits NodeID)
message = Message(id=NODE_ID, data="test".encode("utf-8"), extended=True)
# Send_success means that was stored in the TX Buffer
# It doesn't means that it was successfully sent over the wire!
send_success = canbus.send(message) 
print("Send success:", send_success ) 

# Wait a bit before checking wire emitting!
sleep_ms( 500 )

print( 'transmit_error_count :', canbus.transmit_error_count )
if canbus.transmit_error_count>=100: # Goes up to 128
	raise Exception("Too much transmission error! Is there a receiver on the bus?")

print("That s all folks!")

