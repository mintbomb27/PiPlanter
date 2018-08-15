import RPi.GPIO as GPIO
import dht11
from decimal import Decimal
from gpiozero import LightSensor
import time
import MySQLdb

#GPIO Configurations
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
instance = dht11.DHT11(pin=4)
ldr = LightSensor(14)

#Connecting to MySQL
db = MySQLdb.connect("localhost","root","manuvava","PP")
cursor = db.cursor()

#Updating the Values
while 1>0:
	value_ldr = round(Decimal(10*ldr.value),2) #LDR Value Rounded to 2 Decimals
	result = instance.read()
	if result.is_valid():
		temp = result.temperature # temperature
		humid = result.humidity   # humidity
	update = "UPDATE PiPlanter SET Light='%s',Temperature='%s',Humidity='%s';" % (str(value_ldr),str(temp),str(humid))
	print update
	cursor.execute(update)
	db.commit()
	time.sleep(1)
