import cv2 as cv
import numpy as np
import os
from time import time
import win32gui, win32ui, win32con, win32api

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def window_capture():
    width = win32api.GetSystemMetrics(0)
    height = win32api.GetSystemMetrics(1)

    #hwnd = win32gui,FindWindow(None, windowname)
    hwnd = None
    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj,width,height)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0,0),(width,height),dcObj,(0,0),win32con.SRCCOPY)

    dataBitMap.SaveBitmapFile(cDC,'debug.bmp')

def findClickPosition(template_img_path, target_img_path, threshold = 0.5, debug_mode = 0):

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

'''
loop_time = time()
while(True):
    screenshot = ImageGrab.grab()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot,cv.COLOR_BGR2RGB)
    
    cv.imshow('cv', screenshot)
    print('FPS {}'.format(1 / (time()-loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
'''

window_capture()
print('Done')