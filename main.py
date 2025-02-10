import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision


#WindowCapture.list_window_names()
wincap = WindowCapture('Mabinogi')

# 14 66 241 179 80 250 0 0 0 0
vision_map = Vision('img/map.png')
vision_map.init_control_gui()

while(True):
    screenshot = wincap.get_screenshot()
    
    output_image = vision_map.apply_hsv_filter(screenshot)

    rectangles = vision_map.find(output_image)
    output_image = vision_map.draw_rectangles(output_image,rectangles)

    #display
    resized_map = cv.resize(output_image, (int(wincap.width/2), int(wincap.height/2)), interpolation=cv.INTER_AREA)
    cv.imshow('map',resized_map)

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done')
