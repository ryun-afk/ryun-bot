import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter


#WindowCapture.list_window_names()
wincap = WindowCapture('Mabinogi')

vision_map = Vision('img/map.png')
vision_map.init_control_gui()
filter_map = HsvFilter(14,66,241,179,80,250,0,0,0,0)

loop_time = time()
while(True):
    screenshot = wincap.get_screenshot()
    
    # process images
    processed_image = vision_map.apply_hsv_filter(screenshot,filter_map)
    edges_image = vision_map.apply_edge_filter(screenshot)

    # find object
    rectangles = vision_map.find(screenshot)

    # draw objects detected
    output_image = vision_map.draw_rectangles(screenshot,rectangles)
    
    # keypoint searching
    keypoint_image = edges_image

    # crop the image to remove the ui elements
    x, w, y, h = [200, 1130, 70, 750]
    keypoint_image = keypoint_image[y:y+h, x:x+w]

    kp1, kp2, matches, match_points = vision_map.match_keypoints(keypoint_image)
    match_image = cv.drawMatches(vision_map.target_img, kp1, keypoint_image, kp2, matches, None)

    if match_points:
        # find the center point of all the matched features
        center_point = vision_map.centeroid(match_points)
        # account for the width of the needle image that appears on the left
        center_point[0] += vision_map.target_w
        # drawn the found center point on the output image
        match_image = vision_map.draw_crosshairs(match_image, [center_point])

    # resize images
    scalar = .3
    width = int(wincap.width*scalar)
    height = int(wincap.height*scalar)
    keypoint_image = cv.resize(match_image, (width, height), interpolation=cv.INTER_AREA)
    processed_image = cv.resize(processed_image, (width, height), interpolation=cv.INTER_AREA)
    edges_image = cv.resize(edges_image, (width, height), interpolation=cv.INTER_AREA)

    output_image = cv.resize(output_image, (width, height), interpolation=cv.INTER_AREA)
    output_image = vision_map.apply_hsv_filter(output_image)

    # display image
    cv.imshow('Keypoint Search', keypoint_image)
    cv.imshow('Processed', processed_image)
    cv.imshow('Edges', edges_image)
    cv.imshow('Matches', output_image)

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
print('Done')
