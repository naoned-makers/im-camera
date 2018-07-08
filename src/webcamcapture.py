import cv2

class WebcamCapture(object):
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def next_img(self):
        while True:
            ret, img = self.camera.read()
            yield img

    def clean_iteration(self):
        None

