#!/usr/bin/python

"""
    Main module of the camera feature
"""
import sys
import getopt
import facedetect as fd
import trackperson as tp
import commandrobot as cr
import transformimage as ti
import cv2

MIN_TRACKING_SIZE = 35
PLATFORM_RPI = 'rpi'
PLATFORM_WEBCAM = 'webcam'
PLATFORM_VIDEO = 'video'
MAX_NB_IMG_STOP = 100
MAX_NB_IMG_BEFORE_RECHECK = 100

def main(argv):
    """
        Main function that do the OpenCV loop on the camera images stream

        parameters
        -------------------
        argv : should contains parameters to configure the broker
                -p : the platform (rpi, webcam, video)
                -v : video path
                -b : broker hostname
                -d : headless
    """
    
    #Read the parameters
    tracker = None
    headless = False
    platform = PLATFORM_RPI
    hostname = None
    video_path = None

  
    try:
        opts, args = getopt.getopt(argv,"p:v:b:d",["video_path=","broker_hostname=","platform="])
    except getopt.GetoptError:
        print ('main.py -p <platform> -v <video_path> -b <broker_hostname> -d')
        sys.exit(2)

    for opt, arg in opts:
      if opt in ("-b", "--broker_hostname"):
        hostname = arg
      elif opt in ("-p", "--platform"):
        platform = arg
      elif opt in ("-v", "--video_path"):
        video_path = arg
      elif opt == "-d":
        headless = True

    robot = cr.CommandRobot(hostname)
    source = None

    if platform == PLATFORM_RPI:
        import picapture as cp
        source = cp.PiCapture()
    elif platform == PLATFORM_WEBCAM:
        import webcamcapture as wp
        source = wp.WebcamCapture()
    elif platform == PLATFORM_VIDEO:
        import videocapture as vp
        source = vp.VideoCapture(video_path)


    if not headless:
        cv2.namedWindow("IronMan-View",cv2.WINDOW_NORMAL)

    nb_ignored_recheck_img=0
    nb_img_stop=0

    for img in source.next_img():

        key = cv2.waitKey(10)
        
        if key==27:
            break

        if not tracker:
            rects = fd.detect_faces(img, headless)

            # A face was detected and the tracker is Not following
            if len(rects) > 0 and tracker is None:  
                print ("Start tracking at {}".format(rects[0]))
                #croped_img=crop_img = img[rects[0][1]:rects[0][3], rects[0][0]:rects[0][2]]
                #img_transformed = ti.transform_image(img)
                #img_transformed=img	
                #img_str = cv2.imencode('.jpg', img_transformed)[1].tostring()
                #robot.post_photo(img_str)
                tracker = tp.TrackApp(img,rects[0], headless)

                #Substract last move percent value to 100% to do the mirrored action (person is in front of the head)
                robot.move(tracker.get_last_move_in_percent())

        # A tracker is following but shouldn't be too small
        elif tracker.is_not_too_small(MIN_TRACKING_SIZE):
            tracker.run(img)

            
            #if move is enough significant, move the head to the current tracked face position (pos or neg move)
            if tracker.is_enougth_move():

                #if max nb img before recheck is hitten, send a face detect 
                if tracker.is_always_face():
                    tracker.set_last_move_position_as_current()

                    #Substract last move percent value to 100% to do the mirrored action (person is in front of the head)
                    robot.move(tracker.get_last_move_in_percent())

                    nb_img_stop = 0
                else :
                    tracker=None
                
            elif nb_img_stop == MAX_NB_IMG_STOP:
                print("Stop tracking because camera is waiting too long time")
                tracker=None
                nb_img_stop = 0
            else:
                nb_img_stop += 1        
        else:
            print ("Stop tracking at {}".format(tracker.selection))
            tracker=None

        if not headless:
            cv2.imshow('IronMan-View', img)  
        else:
            cv2.imwrite('/tmp/camera-out.jpg', img)

        source.clean_iteration()

    source.release()
    cv2.destroyAllWindows()
    robot.close()

if __name__ == "__main__":
    main(sys.argv[1:])
