#!/usr/bin/env python

from decimal import Decimal
from gpiozero import LightSensor
import time
import MySQLdb
import serial
import os

ldr = LightSensor(14)
db = MySQLdb.connect("localhost","root","manuvava","PP")
cursor = db.cursor()
os.system("sudo rfcomm connect hci0 98:D3:37:00:8D:E8 1 &")
time.sleep(2)
blueSer = serial.Serial("/dev/rfcomm0", baudrate=9600)
squery = "SELECT Light FROM Configs WHERE cID=1;"

while True:
	valued = round(Decimal(10*ldr.value),2)
	print valued
	cursor.execute(squery)
	result = cursor.fetchall()
	for row in result:
		light = row[0]
	print int(light)
	if valued>int(light) and c==2:
		blueSer.write("n")
		c = 1
		print "Greater"
	elif valued<int(light):
		blueSer.write("y")
		c = 2
		print "Fine"
	else:
		print "Error "+str(c)
	sql = "UPDATE PiPlanter SET Light='%s';" % str(valued)
	cursor.execute(sql)
	db.commit()
	time.sleep(1)
