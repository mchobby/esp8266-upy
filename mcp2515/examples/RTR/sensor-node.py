# --- RTR Sensor node  ----------------------------
# RTR Sensor node waits for RTR request then send the
# the requested data.
#
# The script will listen the CAN bus to:
# - first wait for RTR request for  (NodeID=0x100A002F)
# - Simulate the sensor measurement
# - Send back the measurement data
from machine import SPI,Pin,ADC, idle
from canio import Message, RemoteTransmissionRequest
from mcp2515 import MCP2515
from time import sleep_ms
import struct

atm_pressure_node_id = 0x100A002F # NodeID : Identifies the type of message/data

# Raspberry Pico
spi = SPI( 0, mosi=Pin.board.GP7, miso=Pin.board.GP4, sck=Pin.board.GP6 )
cs = Pin( Pin.board.GP5, Pin.OUT, value=True )
silent = Pin( Pin.board.GP3, Pin.OUT, value=False ) 
canbus = MCP2515( spi, cs, debug=False)  

sensor = ADC(4) # Internal sensor temperature on the Pico

print('Sensor node ready for requests...')
# Will be set True when RTR is received for the sensor
sensor_rtr = False 
while True:
    # Usual processing mix listening + sending phases
    with canbus.listen(timeout=1.0) as listener:
        # Process the received messages
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
        #   use the internal temp. sensor instead of an athmospheric pressure sensor
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

