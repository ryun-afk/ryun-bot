import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision

#WindowCapture.list_window_names()
wincap = WindowCapture('Mabinogi')
cascade_mobs = cv.CascadeClassifier('cascade/cascade.xml')
vision_mobs = Vision(None)

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()

    # resize images
    scalar = .3
    width = int(wincap.width*scalar)
    height = int(wincap.height*scalar)
    screenshot = cv.resize(screenshot, (width, height), interpolation=cv.INTER_AREA)

    rectangles = cascade_mobs.detectMultiScale(screenshot)
    detection_image = vision_mobs.draw_rectangles(screenshot,rectangles)

    # display image
    cv.imshow('original', detection_image)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('y'):
        cv.imwrite('positive/{}.jpg'.format(loop_time), screenshot)
    elif key == ord('u'):
        cv.imwrite('negative/{}.jpg'.format(loop_time), screenshot)

print('Done')
