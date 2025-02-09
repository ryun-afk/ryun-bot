import cv2 as cv
import numpy as np

class Vision:
    target_img = None
    target_w = 0
    target_h = 0
    method = None


    def __init__(self, target_img_path, method=cv.TM_CCOEFF_NORMED):


        self.target_img = cv.imread(target_img_path,self.method)
        self.target_w = self.target_img.shape[1]
        self.target_h = self.target_img.shape[0]

        # TM_CCOEFF, TM_CCOEFF_NORMED, TM_CCORR, TM_CCORR_NORMED, TM_SQDIFF, TM_SQDIFF_NORMED
        self.method = method


    def find(self, template_img, threshold = 0.5, debug_mode = 0):

        result = cv.matchTemplate(template_img, self.target_img, self.method)

        locations = np.where(result >= threshold)
        locations = [(x,y) for x,y in zip(locations[1],locations[0])]

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]),self.target_w,self.target_h]
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles,groupThreshold=1,eps=0.5)
        
        points = []
        if len(rectangles):

                marker_color = (0,0,255)
                marker_type = cv.MARKER_CROSS
                
                line_color = (0,255,0)
                line_type = cv.LINE_4
                
                for (x,y,w,h) in rectangles:
                    center_x = x + int(w/2)
                    center_y = y + int(h/2)
                    points.append((center_x,center_y))
                    
                    if debug_mode == 1:
                        cv.drawMarker(template_img, (center_x,center_y), marker_color, marker_type)
                        
                    elif debug_mode == 2:
                        topleft = (x,y)
                        bottomright = (x+w,y+h)
                        cv.rectangle(template_img,topleft,bottomright, line_color, line_type)

        if debug_mode:
            cv.imshow('debug',template_img)
        
        return points