import cv2 as cv
import numpy as np
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

needle = cv.imread('image.png',cv.IMREAD_UNCHANGED)
hay = cv.imread('image copy.png',cv.IMREAD_UNCHANGED)

result = cv.matchTemplate(hay,needle,cv.TM_CCOEFF_NORMED)


threshhold = 0.80
locations = np.where(result >= threshhold)

locations = [(x,y) for x,y in zip(locations[1],locations[0])]
print(locations)


if locations:
    print('found')

    w = needle.shape[1]
    h = needle.shape[0]

    line_color = (0,255,0)
    line_type = cv.LINE_4

    for loc in locations:
        topleft = loc
        bottomright = (topleft[0]+w, topleft[1] +h)

        cv.rectangle(hay,topleft,bottomright,line_color,line_type)

    cv.imshow('matches',hay)
    cv.waitKey()

else:
    print('not found')