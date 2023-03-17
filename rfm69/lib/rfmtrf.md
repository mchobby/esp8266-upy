# RFM69 Transfert toolbox

This class & methods of [rfmtrf.py](rfmtrf.py) library are aimed to transfer data wider than RFM packet size (limited to 60 bytes).

# RadioHead User Flags

| Constant | Value         |  Description |
|----------|---------------|--------------|
| F_NONE   | 0b0000 (0x0)  | None         |
| F_RESET  | 0b1111 (0xF)  | __Reset__ destination, clear all registers, restart any treatment (like file transfert)  |
| F_EXIT   | 0b1110 (0xE)  | __Exit__ any treatement and return to callee |
| F_SET_REG| 0b0001 (0X1)  | Set a register at remote. data[0] contains register id, data[1..60] the value |
| F_GET_REG| 0b0010 (0x2)  | Get a register from remote. data[0] contains register id |
| F_DATA   | 0b0011 (0x3)  | data packet  |
| F_LASTERR| 0b0111 (0x7)  | Request the last error at destination. Always resetted when readed |   

__Register 0x00__ :
Register 0x00 is common to ALL implementation! Service identification. Data[0] contains the service requested when writing.
IF the destinatory doesn't support the service mentionned in data[0] THEN it returns an error flag with the ACKnowledgment.

* service 0x01 : file transfert to destination.

# File Transfer

Reg 0x01 : filename to be transfered
Reg 0x0A : Data transfer control register
						- 0x01 ready to start file data transfert.
						- 0x02 close file (transfert finished).

ERR 0x10 : needed register not initialized before data transfert
ERR 0x11 : invalid value for 0x0A
