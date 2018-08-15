bluetoothSerial = serial.Serial("/dev/rfcomm0", baudrate=9600)
while 1>0:
	bluetoothSerial.write(raw_input("Please enter "))
#bluetoothSerial.readline()
