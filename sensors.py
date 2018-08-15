import RPi.GPIO as GPIO
import dht11
from decimal import Decimal
from gpiozero import LightSensor
import time
import MySQLdb
import serial
import os

# configs for dht11
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=4)

select = "SELECT Temperature,Light from Configs WHERE cID=1;"

htemp = 30
hhumid = 33
c = 0
d = 0
ldr = LightSensor(14)
db = MySQLdb.connect("localhost","root","manuvava","PP")
cursor = db.cursor()
os.system("sudo rfcomm connect hci0 98:D3:37:00:8D:E8 1 &")
time.sleep(1)
blueSer = serial.Serial("/dev/rfcomm0", baudrate=9600)
while 1>0:
	valued = round(Decimal(10*ldr.value),2)
	result = instance.read()
	if result.is_valid():
		htemp = result.temperature
		hhumid = result.humidity
	cursor.execute(select)
	aresult = cursor.fetchall()
	for row in aresult:
		temp = row[0]
		light = row[1]
	if(temp!="" and light!=""):
		if(htemp>=int(temp) or valued>int(light)):
			blueSer.write("n")
			d = 1
			print "Greater"
			if(htemp>=int(temp)):
				print(htemp)
			elif(valued>int(light)):
				print(light)
		elif(htemp<int(temp) or valued<int(light)):
			blueSer.write("y")
 			d = 2
			print "Fine"
		#else:
			#print "Error"
	else:
		print "Sorry! Couldn't compare"
	update = "UPDATE PiPlanter SET Light='%s',Temperature='%s',Humidity='%s';" % (str(valued),str(htemp),str(hhumid))
	print update
	cursor.execute(update)
	db.commit()
	time.sleep(1)
