"""
trida Comm ziskava informace z arduina
"""

import serial

class Comm:
    def __init__(self, COM, baudrate):
        self.ser = serial.Serial(COM, baudrate, timeout = 1)
        self.ser.baudrate=baudrate
        self.ser.flushInput()
        self.ser.flushOutput()

        self.oldData = 0,0,0,0,0

    #b'|19,-52,-22,0,0|\r\n'
    def read(self):
        try:
            output = self.ser.readline().split("|").decode("utf-8")
            print(output)
            data = output[1].split(",")

            x = int(data[0])
            y = int(data[1])
            z = int(data[2])
            takeShot = int(data[3])
            record = int(data[4])

            self.oldData = x,y,z
            return x,y,z,takeShot,record
        except:
            return self.oldData[0],self.oldData[1],self.oldData[2],0,0

