from maps import ranking

print( "-"*40 )
for val in range( -5, 45, 3 ): # From -5 to 44 by step of 3
	r = ranking( val, [10,20,30,40] )
	print( "%i => %r" %(val,r) )

print( "-"*40 )
for val in range( -5, 45, 3 ): # From -5 to 44 by step of 3
	r = ranking( val, [10,20,30,40], ["A","B","C","D"] )
	print( "%i => %r" %(val,r) )

# Example here upper can be rewitten as follow
# because string are like arrays/list.
#
#for val in range( -5, 45, 3 ): 
#	r = ranking( val, [10,20,30,40], "ABCD" )
#	print( "%i => %r" %(val,r) )