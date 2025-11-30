from machine import SPI,Pin
from canio import Message, RemoteTransmissionRequest
from mcp2515 import MCP2515
from time import sleep_ms

NODE_ID = 0x1234ABCD # NodeID : Identifies the type of message/data

# Raspberry Pico
spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False ) 

canbus = MCP2515( spi, cs, debug=False) 

print('Sending...')
i = 0
while True:
    # Usual processing mix listening + sending phases
    with canbus.listen(timeout=1.0) as listener:
        # Sending a message (extended=True means that we use 29bits NodeID)
        message = Message(id=NODE_ID, data=str(i).encode("utf-8"), extended=True)
        send_success = canbus.send(message)
        print("Send 1 success:", send_success)

        sleep_ms(30)

        # Sending a message as another node (0xAA)
        message = Message(id=0xAA, data=str(1000+i).encode("utf-8"), extended=True)
        send_success = canbus.send(message)
        print("Send 2 success:", send_success)

        sleep_ms(1000)
        i = i + 1

