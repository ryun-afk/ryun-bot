import cv2 as cv
import pyautogui

from time import sleep, time
from threading import Thread, Lock
from math import sqrt

class MachineState:
    INITIALIZING = 0
    SEARCHING = 1
    MOVING = 2
    ACTION = 3
    BACKTRACKING = 4

class Machine:
    # constants
    INITIALIZING_SECONDS = 6
    ACTION_SECONDS = 14
    MOVEMENT_STOPPED_THRESHOLD = 0.975
    IGNORE_RADIUS = 130
    
    # threading properties
    state = None
    targets = []
    screenshot = None
    timestamp = None
    movement_screenshot = None
    window_offset = (0,0)
    window_width = 0
    window_height = 0
    click_history = []

def __init__(self,window_offset,window_size):
    self.lock = Lock()
    self.window_offset = window_offset
    self.window_width = window_size[0]
    self.window_height = window_size[1]

    self.state = MachineState.INITIALIZING
    self.timestamp = time()

def move(self):
    pyautogui.hold('a',5)

    return 

# threading methods
def update_targets(self, targets):
    self.lock.acquire()
    self.targets = targets
    self.lock.release()

def update_screenshot(self, screenshot):
    self.lock.acquire()
    self.screenshot = screenshot
    self.lock.release()

def start(self):
    self.stopped = False
    t = Thread(target=self.run)
    t.start()

def stop(self):
    self.stopped = True
