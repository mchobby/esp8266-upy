#!/bin/sh
SER="/dev/ttyACM0"
echo "Copy to $SER..."

for entry in `ls *.py`; do
	 mpremote connect $SER fs cp $entry :/lib/$entry
done

mpremote connect $SER fs cp mshell.txt :/lib/mshell.txt

echo "Copy WebREPL to $SER..."
cd ..
mkdir tmp
cd tmp
wget -N https://raw.githubusercontent.com/micropython/micropython/master/extmod/webrepl/webrepl.py
wget -N https://raw.githubusercontent.com/micropython/micropython/master/extmod/webrepl/webrepl_setup.py
mpremote connect $SER fs cp webrepl.py :webrepl.py
mpremote connect $SER fs cp webrepl_setup.py :webrepl_setup.py
rm webrepl.py
rm webrepl_setup.py

cd ..
rmdir tmp

echo "Copy Wifi Boot sample to $SER..."
cd examples
mpremote connect $SER fs cp wifi_cfg.sample :wifi_cfg.sample
mpremote connect $SER fs cp boot.timeout.sample :boot.timeout.sample

cd ..
cd lib
