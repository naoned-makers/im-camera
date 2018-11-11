import cv2

class VideoCapture(object):
    def __init__(self, video_path):
        self.camera = cv2.VideoCapture(video_path)

    def next_img(self):
        while True:
            ret, img = self.camera.read()
            yield img

    def clean_iteration(self):
        None

