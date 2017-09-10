import cv2
import numpy as np

def get_center_trackwindow(trackwindow):
    """
        Get center of a track window given as a tuple of :
        (xmin, ymin, width, height)
    """
    return (trackwindow[0]+(trackwindow[2]/2),trackwindow[1]+(trackwindow[3]/2))
    

class TrackApp(object):
    def __init__(self, ref_img, rect):
        xmin, ymin, xmax, ymax = rect[0], rect[1], rect[2], rect[3]

        self.selection = (xmin, ymin, xmax, ymax)
        self.track_window = (xmin, ymin, xmax - xmin, ymax - ymin)
        self.center = get_center_trackwindow(self.track_window)
        
        hsv = cv2.cvtColor(ref_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))   

        x0, y0, x1, y1 = self.selection
        hsv_roi = hsv[y0:y1, x0:x1]
        mask_roi = mask[y0:y1, x0:x1]
        hist = cv2.calcHist( [hsv_roi], [0], mask_roi, [16], [0, 180] )
        cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
        self.hist = hist.reshape(-1)
        
        vis_roi = ref_img[y0:y1, x0:x1]
        cv2.bitwise_not(vis_roi, vis_roi)
        ref_img[mask == 0] = 0


    def show_hist(self, img):
        bin_count = self.hist.shape[0]
        bin_w = 24
        img = np.zeros((256, bin_count*bin_w, 3), np.uint8)
        for i in xrange(bin_count):
            h = int(self.hist[i])
            cv2.rectangle(img, (i*bin_w+2, 255), ((i+1)*bin_w-2, 255-h), (int(180.0*i/bin_count), 255, 255), -1)
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)

    def is_not_too_small(self,size):
        return self.track_window[2]>size and self.track_window[3]>size

    def run(self, new_img):

        hsv = cv2.cvtColor(new_img, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)), np.array((180., 255., 255.)))   

        prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
        prob &= mask
        term_crit = ( cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1 )
        
        track_box, self.track_window = cv2.CamShift(prob, self.track_window, term_crit)    
        
        try:
            cv2.ellipse(new_img, track_box, (0, 0, 255), 2)
        except:
           print(track_box)
        
        self.center=get_center_trackwindow(self.track_window)
        cv2.circle(new_img,self.center, 10, (0,0,255), -1)