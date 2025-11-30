# Using CAN BUS with MCP2515 under MicroPython

[Ce fichier existe également en FRANCAIS](readme.md)

![CAN logo](docs/CAN-logo.jpg)

The CAN bus (Controller Area Network) is a two wire communication network offering reliable data transmission from 0 to 64 bits. This bus is used in a large variety industrial & robotic application, automotive and railway model.

# CAN breakout
The CAN-SPI-BRK is a breakout board using the MCP2515 CAN controler over a SPI BUS. 

The CAN-SPI-BRK is designed for 3V3 logic and designed to built a ready-to-use CAN bus.

![CAN-SPI-BRH BAN bus breakout](docs/CAN-SPI-BRK-01.png)

The controler is able to manage the buffering and transmission of 3 output messages as well as 2 input message.

The board also have:

* the 120Ω terminator resistor (can be distabled.
* the transceiver to convert the MCP2515 signals to CAN-H and CAN-L.
* the ESD protection for CAN-H and CAN-L lines.
* A 5V step-up regulator to power-up the CAN bus (100mA max)

## Credit
The library used with the breakout is based on the [microPython_MCP2515](https://github.com/capella-ben/microPython_MCP2515) work of _capella-ben_ published under the MIT license.
This implementation and attached documentation keeps the MIT license.

# Minimal CAN setup
Being able to transmit data over your DIY CAN bus requires a minimum hardware and software setup.

![CAN bus minimum Setup](docs/CAN-SPI-minimum-setup.jpg)

Here the rules to follow:

* Connect the CAN-H together (do the same for CAN-L). Sharing a common ground is not a necessity but recommended.
* Each end of the bus must have its terminator resistor activated.
* The two node must be powered and __configured by software__.

It is important to have the both nodes (the two bus-end nodes) properly initialised to get an up-and-running CAN bus. This is required for the sender node to get the ACK bit while transmitting the message (otherwise, the message will be sent again and again over the bus).

# About CAN bus
The CAN bus (Controller Area Network) is a two wire communication network offering reliable data transmission. Normalise with ISO11898, the canbus support Node ID coded over 11bits (CAN 2.0A) or 29 bits (CAN 2.0B). The Node ID is a functional identification designating the __type of data/message__ sent on the bus (eg: motor oil temperature, current gear ratio, air temperature, etc).

![CAN bus topology](docs/CAN-BUS-Topology.jpg)

On a CAN bus, a node can start communication at any moment to publish his own message/data.

The CAN bus offers a data payload from 0 to 64 bits (8 bytes) and an automatic message priority (arbitration) based on the emitted NodeID. In a car, the brake messages are more important than a fuel tank level or flashers messages. 

The CAN NodeID is used as a functional data identification (the __type of message__). The listening nodes must use filters to capture the messages/data of interest (otherwise, the listening node capture all the messages).

Thanks to its flexibility and reliability, the CAN bus is nowadays used in many industrial and embedded applications. The most popular application of the CAN bus are the automotive world and model railways.

The initial CAN standard have been improved with many derived standard (eg: CAN-FD, CAN-XL, SAE J1939, ISO 11898-2, CANopen).

## From electrical perspective

The CAN bus is based on a differential signal transmitted across a pair of twisted wires (say CAN-High and CAN-Low).
 
The final signal is made of the difference between the CAN-High and CAN-Low. This tips make the transmitted signal particularly immune to noise. 

![](docs/CAN-BUS-signal.jpg)

When no action is applied the resulting signal is centred on 2.5V . This is the so called recessive voltage corresponding to High bit (1). Bit 1 is so called a recessive bit (say "value by defaut").

When the voltage is modified then a difference of 2V appears between CAN-H and CAN-L. This action use dominant voltage to create a bit 0 (so named the "dominant bit"). 

During the communication, the bit 1 is a bit by default whereas the bit 0 is the result of a voltage modification. This means that a LOW bit transmission takes over the transmission of a HIGH bit.

## CAN Frame
A rough idea of the general CAN frame structure is always a valuable knowledge when you come to trouble.

![CAN frame structure](docs/CAN-frame.jpg)

* __SoF__ : Start of Frame (1 bit)
* __NodeID__ : it identifies the __type of message__ of the data emitted on the bus. initially coded on 11 bits for CAN 2.0A, It can extend to 29bits for CAN 2.0B (see property `extended=True`. __Remark:__ The content of this field is also used for arbritation!
* __RTR__ : Remote Transmission Request (1 bit). Specific type of frame without data where data is requested for a given NodeID (NodeID identifies the type of message). A pre-configured node (say "the sensor") will then transmit the requested data on the bus.
* __Ctrl__ : Control field that contains the Data Length Code (over 4 bits) + 2 reserved bits.
* __Data__ : from 0 to 64 bits (up to 8 bytes) send in MSBF.
* __CRC__ : the Cyclic redundancy code is calculated on previous bits of the frame. It is used to check the integrity of the data.
* __ACK__ : 2 bits made of an ACK Slot and ACK delimiter. The ACK slot is the place where the node receiving the data can inform the network of the CRC correctness (with a dominant bit written in the ACK slot). No ACK received means that __either__ no CAN hardware (mcp2515) were present to receive the frame, __either__ the message was corrupted during transmission. In such case, the message is automatically re-transmitted by the emitter hardware (mcp2515).
* __EoF__ : end of frame (7 bits).

## Meaning of NodeID

Remember, the NodeID identifies the __type of message__ contained in the frame.

When the message is closely tied to a specific device then the NodeID can be merge with a 'node address' (eg: wheel speed).

However, keep in mind that a specific device can be responsible for several messages, so several NodeID (eg: meteo station send messages for temp., humidity, atmospheric pressure, wind speed, luminosity, UV Index). As a consequence, multiple Node ID may be associated to a single physical device.

## NodeID and arbitration
The device emitting the __lowest NodeID will always gets the priority__ on the bus.

The messages sent on the bus can start at any moment by any participants (decentralized access). Thankfully, the first participant starts with a SoF bit, state that other potential participants can spy! 

When the message initiator write its NodeID, the other participant do still spy bit-by-bit the NodeID written by the initiator.

The CAN arbitration resolves bus access with the bit-by-bit comparison on the NodeID. The device emitting the lowest ModeID will always gets the priority on the bus. 

So when an alternate participant with a lower NodeID want to takes over the communication, it just write its own 0 bit (when the initiator will writes its 1 bit). The 0 bit writing automatically win the arbitration and the alternate participant continue the NodeID writing with its own NodeID. During that time, the initiator stops its own NodeID emission and schedule a "retry later" task.

## Building the CAN bus
The bus is made of a twisted pair of wire connecting the CAN_H & CAN_L terminals.

Connecting the GND between the node is not required. However, sharing a common ground between local devices is a good practice.

__Only the both end node of the CAN bus must have the 120Ω terminator resistor activated__. All the intermediate nodes cannot have any terminator resistor.

![CAN BUS setup](docs/CAN-BUS.jpg)

# Wiring 
## CAN Breakout to Pico
Controling the breakout requires a SPI bus connection (Mosi, Miso, SCK, CSn).

The silent (_slnt_) pin is optional. it may be used to switch the breakout in silent mode (only listen the CAN bus, handy for debugging).

![Connect CAN-SPI-BRK to Raspberry-Pi PICO](docs/CAN-SPI-BRK-to-Pico.jpg)

When not used, the reset (_rst_) pin must be tied to 3.3V .

The 120Ω terminator resistor is activated by default. It can be disabled as necessary by cutting the trace behind the board.

![Disabling the CAN terminator resistor](docs/CAN-SPI-BRK-02.png)

# Basic tests
Remember, testing the breakout requires a valid CAN bus setup (see upper in this document for details).

![CAN bus minimum setup](docs/CAN-SPI-minimum-setup.jpg)

## Loopback testing
The [basic/loopback.py](examples/basic/loopback.py) example is a great way to check the SPI bus wiring and the MCP2515 healness.

It configures the MCP2515, activate the loopback mode then write a message that is immediately read back.

## Listen the CAN
IF you build your own testing CAN bus THEN both ends must have an active and initialized node! A great way to achieve this is to have a message __listener__ at one end and a message __sender__ at the other end.

The [basic/listen.py](examples/basic/listen.py) example listen the messages traveling the CAN bus.

Notice that script shows:

* the NodeID of the message (extended is True for 29 bits NodeID otherwise 11 bits).
* the usual messages with binary conttent of the data field (from 1 tto 8 bytes).
* the RTR messages (Remote Transmission Request) with its length.

``` python
from machine import SPI, Pin
from canio import Message, RemoteTransmissionRequest
from mcp2515 import MCP2515
from time import sleep_ms

NODE_ID = 0x4444BBBB # NodeID : Identifies the type of message/data

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
```

## Writing the CAN - single message
The [basic/send_single.py](examples/basic/send_single.py) send a single message over the CAN. 

The message is known as send when it is transfered into the MCP2515 buffer. That doesn't means that message was properly sent over the bus.

So, the script also checks the `canbus.transmit_error_count` which reports physical transmission error on the CAN.

__Remark:__ if transmission error occured then check the other end of the bus (the node is probably inactive).

``` python
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

print('Sending single message...')

# Sending a message (extended=True means that we use 29bits NodeID)
message = Message(id=NODE_ID, data="test".encode("utf-8"), extended=True)
# Send_success means that was stored in the MCP2515 TX Buffer
# It doesn't means that it was successfully sent over the wire!
send_success = canbus.send(message) 
print("Send success:", send_success ) 

sleep_ms( 500 ) # Wait a bit before checking wire emitting!

print( 'transmit_error_count :', canbus.transmit_error_count )
if canbus.transmit_error_count>=100: # Goes up to 128
	raise Exception("Too much transmission error! Is there a receiver on the bus?")

print("That s all folks!")
```

WHEN a communication error occurs on the wire THEN the MCP2515 doesn't release the attached buffer. The MCP2515 tries to emit the message again and again until successfulness! (then the sending buffer is released).

WHEN `canbus.send(message)` returns False THEN it means that sending buffer can't be allocated on the MCP2515. This is caused by a transmission error on the CAN bus.

## Writing the CAN - continuous messages

The [basic/send.py](examples/basic/send.py) example continuously sends multiple messages over the CAN. 

The script sends messages under __TWO DISTINCT NodeID__.

``` python
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
```

# Remote Transmission Request test
The Remote Transmission Request (RTR) is a special flag in the CAN frame used to request data from a given NodeID.

The __RTR message doesn't contains any data!__ However, the control field (of the CAN frame) contains the DLC (Data Length Code) coding a value from 0 to 8. So the __RTR message can ship an extra value (from 0 to 8) encoded within length field__.

## Test scenario 

The test scenario is based on a display device and a sensor device connected through a CAN bus.

* __sensor_node__ : (NodeID=0x100A002F) WAIT for a RTR request THEN perform a measurement and returns a float value (4 Bytes, C style binary encoding).
* __display_node__ : (no NodeID) Request a sensor_node value every 15 seconds (with a RTR message). Displays the value sent by the sensor_node (NodeID=0x100A002F). 

The following pictures shows the progress of a RTR scenario.

![RTR request](docs/CAN-BUS-RTR-01.jpg)

![RTR request detection](docs/CAN-BUS-RTR-02.jpg)

![RTR node processing](docs/CAN-BUS-RTR-03.jpg)

![RTR node sending data response](docs/CAN-BUS-RTR-04.jpg)

![capture RTR response](docs/CAN-BUS-RTR-05.jpg)

## Sensor_node
The initial goal was to measure the athmospheric pressure. Finally it was simplier to measure the Raspberry-Pi Pico internal temperature.

The [RTR/sensor-node.py](examples/RTR/sensor-node.py) example show below perform the following operations:

* continuously listen the can for incoming message.
* check if received message is a RTR request for the sensor_node (for NodeID=0x100A002F).
* IF no RTR request received THEN restart a new listening.

``` python
from machine import SPI,Pin,ADC, idle
from canio import Message, RemoteTransmissionRequest
from mcp2515 import MCP2515
from time import sleep_ms
import struct

atm_pressure_node_id = 0x100A002F # NodeID : Identifies the type of message/data

# Raspberry Pico
spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False ) # Extra silent Pin for transceiver
canbus = MCP2515( spi, cs, debug=False) 

# Internal sensor temperature on the Pico
sensor = ADC(4) 

print('Sensor node ready for requests...')
sensor_rtr = False # set True when RTR received
while True:
    # Usual processing mix listening + sending phases
    with canbus.listen(timeout=1.0) as listener:
        message_count = listener.in_waiting()
        if message_count == 0:
            continue
        print(message_count, "messages available")
        for _i in range(message_count):
            msg = listener.receive()
            print("Message from ", hex(msg.id), "extended:", msg.extended)
            if isinstance(msg, RemoteTransmissionRequest) and (msg.id==atm_pressure_node_id):
                print("RTR received! length=", msg.length)
                sensor_rtr = True

        if not sensor_rtr:
            idle()
            continue

        # Getting the data from the sensor
        adc_value = sensor.read_u16()
        volt = (3.3/65535) * adc_value
        temperature = 27 - (volt - 0.706)/0.001721
        temperature = round(temperature, 1) # float value
        print( "Measured value", temperature )
        # Convert float to binary
        data = struct.pack('f',temperature) # byte() with len=4
        print( "Binary message", data )

        # Sending the requested message
        message = Message(id=atm_pressure_node_id, data=data, extended=True)
        send_success = canbus.send(message)
        if not send_success:
            print("Send data failure")
        else:
            sensor_rtr = False # wait next RTR message

        idle()
```

The __struct__ library is used to pack/unpack Python data into the corresponding C Style binary encoding. This would made possible the data exchange with any type of system.

When running the REPL will display the following messages:

```
Sensor node ready for requests...
1 messages available
Message from  0x100a002f extended: True  <--- receipt a 0x100a002f related message
RTR received! length= 0                  <--- it is a RTR message! Additional "Length" transmited = 0 
Measured value 21.0                      <--- measurement done by the sensor
Binary message b'\x00\x00\xa8A'          <--- measurement as binary data to transmit
1 messages available
Message from  0x100a002f extended: True
RTR received! length= 0
Measured value 21.0
Binary message b'\x00\x00\xa8A'
1 messages available
Message from  0x100a002f extended: True
RTR received! length= 0
Measured value 21.0
Binary message b'\x00\x00\xa8A'
1 messages available
Message from  0x100a002f extended: True
RTR received! length= 0
Measured value 22.4
Binary message b'33\xb3A'
1 messages available
Message from  0x100a002f extended: True
RTR received! length= 0
Measured value 23.3
Binary message b'ff\xbaA
```

## display_node 

The __display_node__ just capture the messages from NodeID=0x100A002F then decode/unpack float stored into the data. Finally it display it on the REPL.

The script also send a _Remote Transmission Request_ every 15 seconds to NodeID 0x100A002F.

``` python
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
```

When running, the script shows the following output on the REPL output

```
Starting Display node...
First sensor request will be issued in 15 secs...
RTR send for ID 0x100a002f
Message from  0x100a002f extended: True
message data: bytearray(b'\x00\x00\xa8A')
Received value = 21.0

RTR send for ID 0x100a002f
Message from  0x100a002f extended: True
message data: bytearray(b'\x00\x00\xa8A')
Received value = 21.0

RTR send for ID 0x100a002f
Message from  0x100a002f extended: True
message data: bytearray(b'\x00\x00\xa8A')
Received value = 21.0

RTR send for ID 0x100a002f
Message from  0x100a002f extended: True
message data: bytearray(b'33\xb3A')
Received value = 22.4

RTR send for ID 0x100a002f
Message from  0x100a002f extended: True
message data: bytearray(b'ff\xbaA')
Received value = 23.3
```

# Filter and mask
A node listening the CAN doesn't need to handle every message/data transmitted on the CAN. 

On a heavy load CAN, this may cause issue because the application layer may be too slow to handle all the incoming message. Chance are that application do miss relevant messages!

The MCP2515 can perform __hardware filtering__ on NodeID of the receive message. Hardware filtering is performant and only receive the messages matching the filter.

## Test scenario 

The test scenario is based on a [filter/master-node.py](examples/filter/master-node.py) script sending messages to several node_id through a CAN bus. 

The [filter/follower-node.py](examples/filter/follower-node.py) script listen the CAN and use __hardware filtering__ to capture the "traffic_light_AA01" messages. 

The alternate [filter/follower-mask.py](example/filter/follower-mask.py) script append a mask over the filter to capture a range of messages.

## master-node
As visible in the [filter/master-node.py](examples/filter/master-node.py) script, several messages are sent to various node.

``` python
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
```

## follower-node

The [filter/follower-node.py](examples/filter/follower-node.py) script use a __Match__ object to filter the messages on a specific node_id.

The created __Match__ object reference is keeps to avoids unuseful object recreation.

``` python
from machine import SPI, Pin
from canio import Message, Match
from mcp2515 import MCP2515
import time, struct

spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False ) 
canbus = MCP2515( spi, cs, debug=False)

traffic_light_AA01 = 0x100FAA01 #  29bits Node ID 

# Prepare the match, extended is set to True because we are on 29bits
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
```

Which produce the following resuts where only the "traffic_light_AA01" message is received by the listen loop.

```
Listening on 0x100faa01 node...
	Read Buffer 0
Message for  0x100faa01 extended: True
	data: bytearray(b'C')
	value: 67
```

## follower-mask
The [filter/follower-mask.py](examples/filter/follower-mask.py) script use a __Match__ object to filter the messages on a specific node_id (used as based) + selection mask.

The aim is to capture all the _traffic_light_Axxx_ messages.

```
traffic_light_AA01 = 0x100FAA01
traffic_light_AA02 = 0x100FAA02
```

So the 17 first bits of the node_id must match the address to enter the filter. The remaining 12 bits are ignored in the comparison.

Only the __Match__ object creation is different, the additional __mask__ parameter indicates which of the 29bits must be used in the filter.
```
_match1 = Match( address=traffic_light_AA01, mask=0b1111_11111111_11110000_00000000, extended=True )
```

This time, several messages are captured by the script.

```
Listening on 0x100faa01 node with mask 0b1111111111111111000000000000 ...
	Read Buffer 0
Message for  0x100faa01 extended: True
	data: bytearray(b'C')
	value: 67

	Read Buffer 0
Message for  0x100faa02 extended: True
	data: bytearray(b'\x81')
	value: 129
```
# Shopping List
All tests where conducted on the __CAN_SPI_BRK__ board from MC Hobby.

* [CAN_SPI_BRK](https://shop.mchobby.be/fr/nouveaute/2881-breakout-can-bus-alim-du-bus-3v3-spi-.html) from MC Hobby
