""" Display the icons defined in icons8.py to the terminal """
from icons8 import all_icons
from icontls import icon_as_text

for icon in all_icons:
	for line in icon_as_text( icon ):
		print( line )
	print( '' )
	print( '' )
	print( '' )
