# Test the Ring Buffer implementation
#
# Author: DMeurisse
#
# See project source at: https://github.com/mchobby/esp8266-upy/tree/master/LIBRARIAN
#
from ringbuf import RingBuffer

ring = RingBuffer( 300 )

def test_simple():
	global ring
	print("--- Some manipulation on the ring ---" )
	print("Ring Size: %s" % ring.size )
	print("Ring Free: %s" % ring.free )
	print("Adding 10 bytes...")
	print("%i bytes written" % ring.put_bytes( bytes([1,2,3,4,5,6,7,8,9,10]) ) )
	print("Ring Free: %s" % ring.free )
	print("Reading 5 bytes...")
	print( ring.get_bytes( 5 ) ) # Read 5 bytes
	print("Ring Free: %s" % ring.free )
	print("Reading 5 bytes...")
	print( ring.get_bytes( 5 ) ) # Read 5 bytes
	print("Ring Free: %s" % ring.free )
	print( "" )

	print("index_put: %s" % ring.index_put )
	print("index_get: %s" % ring.index_get )
	print("is_empty : %s" % ring.is_empty )


def test_fill():
	global ring
	print( "--- Filling the ring ---" )
	for i in range(30):
		print( "%i bytes written" % ring.put_from( bytes([1,2,3,4,5,6,7,8,9,10]) ) )
		print("Ring Free: %3i  -  is_full=%s" % (ring.free, ring.is_full ))
	print( "" )
	print( "Read it back" )
	for i in range( 10 ):
		print( "%02i : %s" % (i,ring.get_bytes(30)) )
		print( "       --> Free=%3i     available_for_reading=%3i" % (ring.free, ring.available_for_reading))


def test_overfill():
	global ring
	print( "--- Overfill test ---")
	print( "Fill the ring" )
	for i in range(30):
		print( "%i bytes written" % ring.put_from( bytes([1,2,3,4,5,6,7,8,9,10]) ) )
	print("Ring Free: %s" % ring.free )
	print("Reading 5 bytes...")
	print( ring.get_bytes( 5 ) ) # Read 5 bytes
	print("Ring Free: %s" % ring.free )
	print("Attempt to add 6 bytes --> should be refused" )
	print( "%i bytes written" % ring.put_from( bytes([101,102,103,104,105,106]) ) )
	print("We should still be at 5 bytes free" )
	print("Ring Free: %s" % ring.free )
	print( "%i bytes written" % ring.put_from( bytes([201,202,203,204]) ) )
	print("We should still be at 1 bytes free" )
	print("Ring Free: %s" % ring.free )
	print( 'Write the last byte')
	ring.put( 255 )
	print("Ring Free: %s" % ring.free )

test_simple()
# test_fill()
# test_overfill()
