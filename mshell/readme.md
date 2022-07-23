```
888b     d888 d8b          d8b       .d8888b.  888               888 888
8888b   d8888 Y8P          Y8P      d88P  Y88b 888               888 888
88888b.d88888                       Y88b.      888               888 888
888Y88888P888 888 88888b.  888       "Y888b.   88888b.   .d88b.  888 888
888 Y888P 888 888 888 "88b 888          "Y88b. 888 "88b d8P  Y8b 888 888
888  Y8P  888 888 888  888 888            "888 888  888 88888888 888 888
888   "   888 888 888  888 888      Y88b  d88P 888  888 Y8b.     888 888
888       888 888 888  888 888       "Y8888P"  888  888  "Y8888  888 888

                          FOR MICROPYTHON

Mini Shell (mshell) is a rudimentary shell designed to run accross all
micropython board implementation. It support rudimentary file filesystem
operations and may be a useful tool when dealing with REPL remotely.


Command: Description             : Example
-------+-------------------------+---------------------------------
help   : display help file       : help
cat    : display file content    : cat main.py
cp     : Copy file (binary)      : cp source.py destin.py
edit   : start text editor       : pye main.py
exit   : exit mini-shell         : exit
free   : Free memory             : free
ls     : list files              : ls -OR- ls /lib
more   : paging file display     : more
mv     : Move a file             : move source.py destin.py
rm     : remove/delete file      : rm demo.py
run    : execute python file     : run gp25.py -OR- run gp25 -OR- ./gp25

some command are available as plug-in stored in /lib/__<command>.py

plug-in    : Description                        : Example
-----------+------------------------------------+-------------------------------
ptest      : plug-in demo showing params        : ptest logo.txt 128 -p=120
hexdump    : display file in hexadecimal        : hexdump logo.txt
ifconfig   : display network interfaces details : ifconfig
wifi       : manage Station wifi                : wifi
           :                                    : wifi up, wifi down, wifi scan,
           :                                    : wifi connect SSID PSWD
touch      : create empty file                  : touch data.log
append     : append text to file                : append target.txt "What men?"
uname      : System identification/information  : uname
df         : Disk Free/disk usage               : df -OR- df /sd
```
Help is fully detailled in the file [mshell.txt](lib/mshell.txt).

Start it by key-in `import mshell` from REPL prompt.

# Revision
0.0.6
* list available plug-ins at startup.
* improve documentation
* implement hexdump

0.0.5
* add plugins wifi, ifconfig
* move uname, df, append, touch to plug-ins

0.0.4
* display on 24 lines x 80 columns
* summary of commands + example. One line per command!
* ls, cat, more, ... now supporting path
* ls : now have paging
* free : garbage collect + display free memory
* help : also open mshell.txt from /lib
* more : cat with paging
* ./xxx : execute/reexcute a xxx.py python script (run command)
* plug-in command hexdump (not complete) and ptest (plug in test demo)

# Plug-in

To add a plugin for a new command `ptest`:
* Add the file `__ptest.py` into the `lib` subfolder.
* Define the `ptest( shell, args )` function to implements the command feature.

Here follow the content of the function:

``` python
def ptest( shell, args ):
	shell.println( '--- ptest MiniShell Plug-in demo ---')
	shell.println( 'args count: %s' % len(args) )
	for i in range( len(args) ):
		shell.println( 'args[%i] = %s' % (i, args[i]) )

	# All input should be made via the shell object
	val = shell.readline( 'Your name: ')
	shell.println( 'You entered: %s' % val)

	# Must return a numeric value 0 = OK, >0 = Error
	return 0
```

# TODO list

* mshell -> support args parsing for "aa bbb"
* mshell -> reinforce plug-in startup
* mshell -> fully support sub-directory (cd, pwd)
* mshell -> set : support environment variable
* mshell -> ls : multi columns
* mshell -> ls : display filesize?
* mshell -> reboot
* mshell -> find : find a file (find zumo)
* hexdump.py -> View content of file as HEX

* get.py -> get a file over wifi

Idea: Receive a file over the REPL line (with cat from host: cat file > /dev/ttyACM0 )
