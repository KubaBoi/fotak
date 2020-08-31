#sudo nano /etc/rc.local --- python /var/www/html/fotak/shot.py
from picamera import PiCamera

class Cam:
    def __init__(self):
        self.camera = PiCamera()

        self.camera.rotation = 90
    
    def startPreview(self):
        self.camera.start_preview()
    def stopPreview(self):
        self.camera.stop_preview()

    def recordFrame(self, frameNumber):
        frame = ""
        for i in range(0, 5 - len(str(frameNumber))):
            frame += "0"

        frame += str(frameNumber)
        self.camera.capture("/frames/frame" + frame + ".png")

    def takeShot(self):
        print("Taking shot...")
        self.camera.capture("shot.png")
        print("Shot taken")