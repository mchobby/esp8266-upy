from machine import SPI, Pin
from canio import Message, RemoteTransmissionRequest
from mcp2515 import MCP2515
from time import sleep_ms

NODE_ID = 0x4444BBBB # NodeID : Identifies the type of message/data
#NODE_ID = 0xAA

spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False )

canbus = MCP2515( spi, cs, debug=False)  

print('Listening...')
while True:
    with canbus.listen(timeout=1.0) as listener:
        message_count = listener.in_waiting()
        if message_count == 0:
            continue
        print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            # Display the remote node ID
            print("Message from ", hex(msg.id), "extended:", msg.extended)
            if isinstance(msg, Message):
                print("message data:", msg.data)
            if isinstance(msg, RemoteTransmissionRequest):
                print("RTR length:", msg.length)
            print("")
