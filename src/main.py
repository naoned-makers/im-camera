#!/usr/bin/python

"""
    Main module of the camera feature
"""
import facedetect as fd
import trackperson as tp
import commandrobot as cr
import cv2
import sys, getopt


MIN_TRACKING_SIZE = 35


def main(argv):
    """
        Main function that do the OpenCV loop on the camera images stream

        parameters
        -------------------
        argv : should contains parameters to configure the broker
                -h : the hostname
                -t : the topic name
    """

    camera = cv2.VideoCapture(0)
    cv2.namedWindow("IronMan-View",cv2.WINDOW_NORMAL)
    tracker = None
    robot = cr.CommandRobot()

    #Read the parameters
    try:
        opts, args = getopt.getopt(argv,"ht",["hostname=","topic="])
    except getopt.GetoptError:
        print 'main.py -h <hostname> -t <topic>'
        sys.exit(2)

    for opt, arg in opts:
      if opt in ("-h", "--hostanme"):
         robot.hostname = arg
      elif opt in ("-t", "--topic"):
         robot.topic_name = arg

    while True:
        ret, img = camera.read()
        rects = fd.detect_faces(img)

        key = cv2.waitKey(10)
        
        if key==27:
            break

        # A face was detected and the tracker is Not following
        if len(rects) > 0 and tracker is None:
            print "Start tracking at {}".format(rects[0])
            tracker = tp.TrackApp(img,rects[0])

            #Substract last move percent value to 100% to do the mirrored action (person is in front of the head)
            robot.move(100-tracker.get_last_move_in_percent())

        # A tracker is following
        if tracker:
            # first we test the tracking_box : if it's too small we stop tracking the current person
            if tracker.is_not_too_small(MIN_TRACKING_SIZE):
                tracker.run(img)

                #if move is enough significant, move the head to the current tracked face position (pos or neg move)
                if tracker.is_enougth_move():
                    tracker.set_last_move_position_as_current()

                    #Substract last move percent value to 100% to do the mirrored action (person is in front of the head)
                    robot.move(100-tracker.get_last_move_in_percent())
                
            else:
                print "Stop tracking at {}".format(tracker.selection)
                tracker=None

        cv2.imshow('IronMan-View', img)  

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main(sys.argv[1:])