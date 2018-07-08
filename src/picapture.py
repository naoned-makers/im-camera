import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

class PiCapture(object):
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640,480)
        self.camera.framerate = 32
        
        self.rawCapture = PiRGBArray(self.camera, size=(640,480))
    
        time.sleep(0.1)

    def next_img(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            img = frame.array
            yield img
    
    def clean_iteration(self):
        self.rawCapture.truncate(0)
