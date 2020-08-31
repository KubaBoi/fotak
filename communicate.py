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
            output = self.ser.readline().split("|")[1]
            data = output.split(",")

            x = data[0]
            y = data[1]
            z = data[2]
            takeShot = data[3]
            record = data[4]

            self.oldData = x,y,z,takeShot,record
            return self.oldData
        except:
            return self.oldData

