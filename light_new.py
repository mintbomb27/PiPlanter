import RPi.GPIO as GPIO
import time
import MySQLdb
from decimal import Decimal

mpin=17
tpin=27
GPIO.setmode(GPIO.BCM)

db = MySQLdb.connect("localhost","root","manuvava","PP")
cursor = db.cursor()

cap=0.00000001
adj=2.130620985
i=0
t=0
while True:
    GPIO.setup(mpin, GPIO.OUT)
    GPIO.setup(tpin, GPIO.OUT)
    GPIO.output(mpin, False)
    GPIO.output(tpin, False)
    time.sleep(0.2)
    GPIO.setup(mpin, GPIO.IN)
    time.sleep(0.2)
    GPIO.output(tpin, True)
    starttime=time.time()
    endtime=time.time()
    while (GPIO.input(mpin) == GPIO.LOW):
        endtime=time.time()
    measureresistance=endtime-starttime
    res=(measureresistance/cap)*adj
    i=i+1
    t=t+res
    if i==10:
            t=t/i
	    t=t/100000
	    t=round(Decimal(10-t),2)
	    print t
	    update = "UPDATE PiPlanter SET Light='%s';" % (str(t))
       	    print update
            cursor.execute(update)
            db.commit()
	    t=0
	    i=0
