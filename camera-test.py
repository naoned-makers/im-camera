from picamera import PiCamera
from time import sleep

camera = PiCamera()
#camera.capture('image-test.jpg')

camera.start_preview()

while True:
	sleep(1)
#camera.close()
