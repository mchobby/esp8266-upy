# --- RTR display node  ----------------------------
# RTR Display node acts like an interractive display sensor
# data collected through the CAN bus before display ingit. 
#
# The script displays the sensor measurement (NodeID=0x100A002F).
# - The script will first request data through a CAN bus with
#   a RTR message (Remote Transmit Request).
# - The remote sensor will capture the RTR and repond with a
#   new message containing the data
# - The script will capture the message with data THEN display
#   its data.
from machine import SPI, Pin
from canio import Message, RemoteTransmissionRequest
from mcp2515 import MCP2515
import time, struct

atm_pressure_node_id = 0x100A002F # NodeID : Identifies the type of message/data

spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False ) 

canbus = MCP2515( spi, cs, debug=False)

print('Starting Display node...')
print('First sensor request will be issued in 15 secs...')
start = time.ticks_ms()
while True:
    with canbus.listen(timeout=1.0) as listener:
        # Process the received messages
        message_count = listener.in_waiting()
        # print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            # Display the remote node ID
            print("Message from ", hex(msg.id), "extended:", msg.extended)
            if isinstance(msg, Message) and (msg.id==atm_pressure_node_id):
                print("message data:", msg.data)
                # Decode the float value sent by the sensor node
                values = struct.unpack('f', msg.data ) # Always returns a typle
                print( "Received value =", values[0] )
            print("")

        # Requesting the sensor data every 15 seconds
        if time.ticks_diff( time.ticks_ms(), start ) >= 15000:
            start = time.ticks_ms()
            msg = RemoteTransmissionRequest( id=atm_pressure_node_id, length=0, extended=True )
            send_success = canbus.send(msg)
            print("RTR send for ID", hex(atm_pressure_node_id) )
