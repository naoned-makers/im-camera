import cv2
import numpy as np
import scipy.misc as scmi

JARVIS_IMG_PATH="data/img/kinect_jarvis_invert.png"
VIEWFINDER_IMG_PATH="data/img/viewfinder.png"

def __apply_custom_colormap(im_gray):

    rgb = scmi.imread(JARVIS_IMG_PATH)
    

    lut = np.zeros((256, 1, 3), dtype=np.uint8)
    lut[:, 0, 0] = rgb[1,:,2]
    lut[:, 0, 1] = rgb[1,:,1]
    lut[:, 0, 2] = rgb[1,:,0]


    im_color = cv2.LUT(im_gray, lut)

    return im_color


def transform_image(img):

    img_transformed = __apply_custom_colormap(img)
    cv2.GaussianBlur(img_transformed,(5,5), 0)

    return img_transformed