from cam import Cam
from communicate import Comm
from time import sleep

import serial

cam = Cam()

cam.startPreview()

comm = Comm("/dev/ttyACM0", 115200)

while True:
	#read_ser=ser.readline().decode("utf-8")

	print(comm.read())
