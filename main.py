import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision


#WindowCapture.list_window_names()
wincap = WindowCapture('Mabinogi')
vision_corn = Vision('image.png')

while(True):
    screenshot = wincap.get_screenshot()

    points = vision_corn.find(screenshot,0.5,1)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done')
