# BAsed on https://github.com/elechouse/PN532/blob/PN532_HSU/PN532/PN532Interface.h
#
PN532_PREAMBLE              = const(0x00)
PN532_STARTCODE1            = const(0x00)
PN532_STARTCODE2            = const(0xFF)
PN532_POSTAMBLE             = const(0x00)

PN532_HOSTTOPN532           = const(0xD4)
PN532_PN532TOHOST           = const(0xD5)

# PN532_ACK_WAIT_TIME           const(10)  // ms, timeout of waiting for ACK

PN532_INVALID_ACK           = const(-1)
PN532_TIMEOUT               = const(-2)
PN532_INVALID_FRAME         = const(-3)
PN532_NO_SPACE              = const(-4)

def reverse_bits_order( b ):
	b = (b & 0xF0) >> 4 | (b & 0x0F) << 4
	b = (b & 0xCC) >> 2 | (b & 0x33) << 2
	b = (b & 0xAA) >> 1 | (b & 0x55) << 1
	return b

# Any Hardware Abstraction Layer (HAL) must expose the following public interface
# class PN532Interface
# public:
#    virtual void begin() = 0; --> not implemented
#    virtual void wake_up() = 0;
#    virtual int8_t write_command(const uint8_t *header, const uint8_t *body = 0 ) = 0;
#    virtual int16_t readResponse(uint8_t buf[], uint8_t len, uint16_t timeout = 1000) = 0;
