import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision


#WindowCapture.list_window_names()
wincap = WindowCapture('Mabinogi')
vision_test = Vision('image.png')

while(True):
    screenshot = wincap.get_screenshot()

    rectangles = vision_test.find(screenshot)

    cv.imshow('debug',vision_test.draw_rectangles(screenshot,rectangles))

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done')
