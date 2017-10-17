#!/usr/bin/python

"""
    Main module of the camera feature
"""
import sys
import getopt
import facedetect as fd
import trackperson as tp
import commandrobot as cr
import cv2
from picamera import PiCamera
from picamera.array import PiRGBArray
import time

MIN_TRACKING_SIZE = 35

def main(argv):
    """
        Main function that do the OpenCV loop on the camera images stream

        parameters
        -------------------
        argv : should contains parameters to configure the broker
                -h : the hostname
                -t : the topic name
                -d : headless
    """
    
    #Read the parameters
    tracker = None
    headless = False
    robot = cr.CommandRobot()

  
    try:
        opts, args = getopt.getopt(argv,"htd",["hostname=","topic=", "headless"])
    except getopt.GetoptError:
        print ('main.py -h <hostname> -t <topic> -d')
        sys.exit(2)

    for opt, arg in opts:
      if opt in ("-h", "--hostanme"):
         robot.hostname = arg
      elif opt in ("-t", "--topic"):
         robot.topic_name = arg
      elif opt in ("-d", "--headless"):
         headless = True

    camera = PiCamera()
    camera.resolution = (640,480)
    camera.framerate = 32
    
    rawCapture = PiRGBArray(camera, size=(640,480))
    
    time.sleep(0.1)
    
    if not headless:
        cv2.namedWindow("IronMan-View",cv2.WINDOW_NORMAL)

    nb_ignored_img=0
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array

        key = cv2.waitKey(10)
        
        if key==27:
            break

        if not tracker:         
            rects = fd.detect_faces(img, headless)

            # A face was detected and the tracker is Not following
            if len(rects) > 0 and tracker is None:
                print ("Start tracking at {}".format(rects[0]))
                tracker = tp.TrackApp(img,rects[0], headless)

                #Substract last move percent value to 100% to do the mirrored action (person is in front of the head)
                robot.move(tracker.get_last_move_in_percent())

        # A tracker is following but shouldn't be too small
        elif tracker.is_not_too_small(MIN_TRACKING_SIZE):
            tracker.run(img)

            #if move is enough significant, move the head to the current tracked face position (pos or neg move)
            if tracker.is_enougth_move():
                tracker.set_last_move_position_as_current()

                #Substract last move percent value to 100% to do the mirrored action (person is in front of the head)
                robot.move(tracker.get_last_move_in_percent())        
        else:
            print ("Stop tracking at {}".format(tracker.selection))
            tracker=None

        if not headless:
            cv2.imshow('IronMan-View', img)  
        else:
            cv2.imwrite('/tmp/camera-out.jpg', img)
        rawCapture.truncate(0)

cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])
