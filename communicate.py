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

    #b'|19,-52,-22,0,0|\r\n'
    def read(self):
        output = self.ser.readline().decode("utf-8")
        self.ser.flush()
        self.ser.flushInput()
        self.ser.flushOutput()
        
        data = output.split(",")

        if (len(data) != 5):
            return 0,0,0,0,0

        x = int(data[0])
        y = int(data[1])
        z = int(data[2])
        takeShot = int(data[3])
        record = int(data[4])

        return x,y,z,takeShot,record

