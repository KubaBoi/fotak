#sudo nano /etc/rc.local --- python /var/www/html/fotak/shot.py
from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.rotation = 90
camera.start_preview()
sleep(60)
camera.stop_preview()