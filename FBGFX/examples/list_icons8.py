""" Display the icons defined in icons8.py as a list of [True,False,True,...] values in the terminal """
from icons8 import all_icons
from icontls import icon_as_list

for icon in all_icons:
	for l in icon_as_list( icon ):
		print( l )
	print( '' )
	print( '' )
	print( '' )
