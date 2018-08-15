import RPi.GPIO as GPIO
import MySQLdb
import time
import dht11
from decimal import Decimal

#Database Configs
db= MySQLdb.connect("localhost","root","manuvava","PP")
cursor = db.cursor()
select = "SELECT Moisture from PiPlanter;"
select2 = "SELECT Temperature,Light from Configs WHERE cID=1;"
max_light = 6
max_temp = 30

#GPIO Configs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(18, GPIO.OUT) # Relay 1
GPIO.setup(22, GPIO.OUT) # Relay 2
GPIO.setup(23, GPIO.OUT) # RED led
GPIO.setup(24, GPIO.OUT) # BLUE led
instance = dht11.DHT11(pin=4)
while 1>0:
	mpin=17
        tpin=27
        cap=0.00000001
        adj=2.130620985
        i=0
        t=0
        a=b=0
        while a==b:
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
                        cur_light =round(Decimal(10-t),2)
                        t=0
                        i=0
                        a=1
	nowdht = instance.read()
        if nowdht.is_valid():
                cur_temp = nowdht.temperature
                cur_humid = nowdht.humidity
	cursor.execute(select)
	moisture = cursor.fetchall()
	for row in moisture:
		moist = row[0]
	print moist
	cursor.execute(select2)
	values = cursor.fetchall()
	for arow in values:
		max_temp = arow[0]
		max_light = arow[1]
	if(max_temp!="" and max_light!=""):
		if(cur_light>=int(max_light) or cur_temp>=int(max_temp)):
			GPIO.output(18, 1)
			GPIO.output(22, 1)
			GPIO.output(23, 1)
			time.sleep(1)
			GPIO.output(23, 0)
			time.sleep(1)
			print "Alert!! Values Greater!"
			if(cur_temp>=int(max_temp)):
				print "Temperature : ",cur_temp
			elif(cur_light>=int(max_light)):
				print "Light : ",cur_light
		elif(cur_light<=int(max_light) and cur_temp<=int(max_temp)):
			print "Fine"
			if int(moist)<50:
				GPIO.output(23, 1)
				GPIO.output(24, 0)
				print "Watering..."
				GPIO.output(18, 0)
				GPIO.output(22, 0)
				thetime = str(time.strftime("%I:%M %p %b %d, %a", time.localtime()))
                        	sqll = "UPDATE PiPlanter SET LTime='%s';" % thetime
                        	sqlin = "INSERT INTO History (Time) VALUES ('%s');" % thetime
                        	cursor.execute(sqll)
                        	cursor.execute("SELECT * from History ORDER BY ID DESC LIMIT 1;")
                        	row = str(cursor.fetchone())
                        	if(thetime not in row):
                        	        cursor.execute(sqlin)
			elif int(moist)>50:
				GPIO.output(23, 0)
				GPIO.output(24, 1)
				print "Its Wet!"
				GPIO.output(18, 1)
        	                GPIO.output(22, 1)
			else:
				print "Error in Moisture"
		else:
			print "Error in Comparison"
	else:
		print "Error DB Max_Values NULL"
	update = "UPDATE PiPlanter SET Light='%s',Temperature='%s',Humidity='%s';" % (str(cur_light),str(cur_temp),str(cur_humid))
	print update
	cursor.execute(update)
	db.commit()
