#pussyword qawsedrftgyh
#test

from cam import Cam
from communicate import Comm
from time import sleep

import serial

cam = Cam()

cam.startPreview()

try:
	comm = Comm("/dev/ttyUSB1", 115200)
except:
	comm = Comm("/dev/ttyUSB0", 115200)
#comm = Comm("COM5", 115200)

recording = False
frameNumber = 0

while True:
	x,y,z,takeShot,record = comm.read()

	if (record == 1):
		if (recording):
			recording = False
			print("Recording ended...")
			cam.stopRecording()
		else:
			recording = True
			cam.startRecording()
			print("Recording started...")

	if (takeShot == 1):
		cam.takeShot()