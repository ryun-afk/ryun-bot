import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture



wincap = WindowCapture('Mabinogi')
WindowCapture.list_window_names()

while(True):
    screenshot = wincap.get_screenshot()
    screenshot = np.array(screenshot)
    
    cv.imshow('cv', screenshot)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done')


def find_click_position(template_img_path, target_img_path, threshold = 0.5, debug_mode = 0):

    template = cv.imread(template_img_path,cv.IMREAD_UNCHANGED)
    target = cv.imread(target_img_path,cv.IMREAD_UNCHANGED)
    target_w = target.shape[1]
    target_h = target.shape[0]


    result = cv.matchTemplate(template,target,cv.TM_CCOEFF_NORMED)

    locations = np.where(result >= threshold)
    locations = [(x,y) for x,y in zip(locations[1],locations[0])]


    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]),target_w,target_h]
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles,1,0.5)
    
    points = []

    if len(rectangles):
        for (x,y,w,h) in rectangles:
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x,center_y))

            if debug_mode == 1:
                marker_color = (0,0,255)
                marker_type = cv.MARKER_CROSS
                cv.drawMarker(template, (center_x,center_y), marker_color, marker_type)

            if debug_mode == 2:
                topleft = (x,y)
                bottomright = (x+w,y+h)
                line_color = (0,255,0)
                line_type = cv.LINE_4
                cv.rectangle(template,topleft,bottomright, line_color, line_type)

        if debug_mode > 0:
            cv.imshow('matches',template)
            cv.waitKey()
    
    return points