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