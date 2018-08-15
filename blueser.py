#! /usr/bin/python

import serial
from time import sleep

bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)
usbSerial = serial.Serial("/dev/ttyACM0", baudrate=9600)
count = None
while count == None:
	try:
		count= raw_input("Please enter the no. of times to blink the LED ")
	except:
		pass

bluetoothSerial.write(str(count))
print usbSerial.readline()
