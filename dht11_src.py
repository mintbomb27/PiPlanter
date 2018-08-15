#!/usr/bin/env python

import RPi.GPIO as GPIO
import dht11
import time
import datetime
import MySQLdb

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
db = MySQLdb.connect("localhost","root","manuvava","PP")
cursor = db.cursor()

# read data using pin 14
instance = dht11.DHT11(pin=4)

while True:
    result = instance.read()
    if result.is_valid():
        #print("Last valid input: " + str(datetime.datetime.now()))
        #print("Temperature: %d C" % result.temperature)
        #print("Humidity: %d %%" % result.humidity)
	sql = "UPDATE PiPlanter SET Temperature=%s;" % result.temperature
	sqll = "UPDATE PiPlanter SET Humidity=%s;" % result.humidity
    	cursor.execute(sql)
	cursor.execute(sqll)
	db.commit()
    #else:
	#print("Error!")
    time.sleep(1)
