import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
pin = 12 #input("Enter pin ")
GPIO.setup(12, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
try:
	for i in range(0,10):	
		GPIO.output(pin, GPIO.HIGH)
		GPIO.output(15, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(pin, GPIO.LOW)
		GPIO.output(15, GPIO.LOW)
		time.sleep(1)
except KeyboardInterrupt:
	GPIO.cleanup()
GPIO.cleanup()
