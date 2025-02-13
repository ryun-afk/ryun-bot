import cv2 as cv
from time import time

from windowcapture import WindowCapture
from detection import Detection
from vision import Vision
from machine import Machine, MachineState

DEBUG = True
SCALAR = .5

wincap = WindowCapture('Mabinogi')
detector = Detection('training/cascade/cascade.xml')
vision = Vision()
#machine = Machine((wincap.offset_x,wincap.offset_x),(wincap.width,wincap.height))

wincap.start()
detector.start()
#machine.start()

loop_time = time()
def main():
    while(True):
        if wincap.screenshot is None:
            continue

        detector.update(wincap.screenshot)
        '''
        if machine.state == MachineState.INITIALIZING:
            targets = vision.get_click_points(detector.rectangles)
            machine.update_targets(targets)
        elif machine.state == MachineState.SEARCHING:
            targets = vision.get_click_points(detector.rectangles)
            machine.update_targets(targets)
            machine.update_screenshot(wincap.screenshot)
        elif machine.state == MachineState.MOVING:
            machine.update_screenshot(wincap.screenshot)
        elif machine.state == MachineState.ACTION:
            pass
        '''

        # debug
        if DEBUG:
            detection_image = vision.draw_rectangles(wincap.screenshot, detector.rectangles)
            detection_image = resize(detection_image)
            cv.imshow('Matches', detection_image)

            #print_fps(loop_time)

        # tool
        key = cv.waitKey(1)
        if key == ord('q'):
            wincap.stop()
            detector.stop()
            #machine.stop()
            cv.destroyAllWindows()
            break

def resize(img):
    width = int(wincap.width*SCALAR)
    height = int(wincap.height*SCALAR)
    return cv.resize(img, (width, height), interpolation=cv.INTER_AREA)

def print_fps(loop_time):
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

main()
#WindowCapture.list_window_names()
print('Done')
