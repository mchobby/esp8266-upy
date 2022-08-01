""" MiniShell ifconfig command. """

def ifconfig( shell, args ):
	# All input should be made via the shell
	try:
		import network
	except:
		shell.println( 'No network support!' )
		return -1

	sta = network.WLAN( network.STA_IF )
	ap = network.WLAN( network.AP_IF )

	shell.println( "Access Point: %s" % ('ACTIVE' if ap.active() else 'inactive') )
	if ap.active():
		shell.println( "   %r" % ap )
		_ip, _mask, _gateway, _dns = ap.ifconfig()
		shell.println( "   IP     : %s" % _ip )
		shell.println( "   NetMask: %s" % _mask )
		shell.println( "   Gateway: %s" % _gateway )
		shell.println( "   DNS    : %s" % _dns )
	shell.println( "Station mode: %s" % ('ACTIVE' if sta.active() else 'inactive') )
	if sta.active():
		shell.println( "   %r" % sta )
		_ip, _mask, _gateway, _dns = sta.ifconfig()
		shell.println( "   IP     : %s" % _ip )
		shell.println( "   NetMask: %s" % _mask )
		shell.println( "   Gateway: %s" % _gateway )
		shell.println( "   DNS    : %s" % _dns )

	# Must return a numeric value 0 = OK, >0 = Error
	return 0
