#!/usr/bin/env python
from __future__ import division
import serial
import sys, os
import re, time
import MySQLdb

ser = serial.Serial('/dev/ttyACM0',9600)
#ser.open()
db = MySQLdb.connect("localhost","root","manuvava","PP")
cursor = db.cursor()

try:
	while True:
		moisture=int(ser.readline())
		#print moisture
		moist = str(int(100-(moisture/1024*100)))+"%"
		#print("Soil Moisture: "+moist)
		sql = "UPDATE PiPlanter SET Moisture='%s';" % moist
		cursor.execute(sql)
		if(moisture>500):
			thetime = str(time.strftime("%I:%M %p %b %d, %a", time.localtime()))
			sqll = "UPDATE PiPlanter SET LTime='%s';" % thetime
			sqlin = "INSERT INTO History (Time) VALUES ('%s');" % thetime 
			cursor.execute(sqll)
			cursor.execute("select * from History ORDER BY ID DESC LIMIT 1;")
			row = str(cursor.fetchone())
			if(thetime not in row):
				cursor.execute(sqlin)
		db.commit()
except KeyboardInterrupt:
	print "Thank You!"
	sys.exit(0)
