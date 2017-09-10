import facedetect as fd
import trackperson as tp
import cv2


MIN_TRACKING_SIZE=35
IMG_X_MOVE_EVENT=100


def main():

    camera = cv2.VideoCapture(0)
    cv2.namedWindow("IronMan-View",cv2.WINDOW_NORMAL)
    tracker = None
    last_x_event = None

    while True:
        ret, img = camera.read()
        rects = fd.detect_faces(img)

        key = cv2.waitKey(10)
        

        # A face was detected and the tracker is Not following
        if len(rects) > 0 and tracker is None:
            print "Start tracking at {}".format(rects[0])
            tracker = tp.TrackApp(img,rects[0])

            #TODO : align IM's head with the tracked face   


        if key==27:
            break

        # A tracker is following
        if tracker:
            # first we test the tracking_box : if it's too small we stop tracking the current person
            if tracker.is_not_too_small(MIN_TRACKING_SIZE):
                tracker.run(img)

                #TODO : if move is enough significant, move the head to the current tracked face position (pos or neg move)
                
            else:
                print "Stop tracking at {}".format(tracker.selection)
                tracker=None

        cv2.imshow('IronMan-View', img)  

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()