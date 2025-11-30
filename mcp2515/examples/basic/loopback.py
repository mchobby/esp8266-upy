from time import sleep
from machine import SPI,Pin
from canio import Message, RemoteTransmissionRequest
from mcp2515 import MCP2515


# Raspberry Pico
spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT ) # Extra silent Pin for transceiver

canbus = MCP2515( spi, cs, loopback=True, silent=True, silent_pin=silent, debug=False)  # use loopback to test without another device


i = 0
while True:
    with canbus.listen(timeout=1.0) as listener:

        message = Message(id=0x1234ABCD, data=b"data" + bytes([i]), extended=True)
        sendResult = canbus.send(message)
        print("Send success:", sendResult)
        
        
        message_count = listener.in_waiting()
        print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            print("Message from ", hex(msg.id))
            if isinstance(msg, Message):
                print("message data:", msg.data)
            if isinstance(msg, RemoteTransmissionRequest):
                print("RTR length:", msg.length)
    sleep(1)
    i = i + 1
