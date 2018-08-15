from gpiozero import LightSensor
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.cleanup()
ldr = LightSensor(22)
while 1>0:
	#ldr = LightSensor(17)
	print ldr.value
	time.sleep(1)
GPIO.cleanup()
