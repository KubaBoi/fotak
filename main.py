from cam import Cam
from communicate import Comm
from time import sleep

import serial

cam = Cam()

cam.startPreview()

comm = Comm("/dev/ttyUSB0", 115200)
while True:
	x,y,z,takeShot,record = comm.read()
	if (record == 1):
		print("penis")
