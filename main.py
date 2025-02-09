import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision


#WindowCapture.list_window_names()
wincap = WindowCapture('Mabinogi')
vision_test = Vision('image.png')
vision_test.init_control_gui()

while(True):
    screenshot = wincap.get_screenshot()

    #object detection
    rectangles = vision_test.find(screenshot)
    points = vision_test.get_click_points(rectangles)

    #draw on image
    #output_image = vision_test.draw_click_points(screenshot,points)
    output_image = vision_test.apply_hsv_filter(screenshot)

    #display processed image
    cv.imshow('debug',output_image)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done')
