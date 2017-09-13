import cv2

# Initialize the face detection algorithme with configuration to detect frontal face
face_cascade = cv2.CascadeClassifier('data/haarcascades/haarcascade_frontalface_alt.xml')

# Detect all faces in the current image with an opencv cascade algorithme  
# return an array of rects
def detect(img, cascade):
    rects = cascade.detectMultiScale(img, scaleFactor=1.3, minNeighbors=4, minSize=(30, 30),
                                     flags=cv2.CASCADE_SCALE_IMAGE)
    if len(rects) == 0:
        return []
    rects[:,2:] += rects[:,:2]
    return rects

# Draw a rectangle for all the detected face on the current image
def draw_rects(img, rects, color):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)


# Global function to detect all faces in a image
def detect_faces(img):
    """
        Detects all the faces in the current img
        return an array of the rectangles surrounding the detected faces
    """

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)

    rects = detect(gray, face_cascade)
    draw_rects(img, rects, (0, 255, 0))
    
    return rects