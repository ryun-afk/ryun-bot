import cv2 as cv
from threading import Thread, Lock

class Detection:
    # threading properties
    stopped = True
    lock = None
    rectangles = []

    # properties
    cascade = None
    screenshot = None

    def __init__(self,model_file_path):
        self.lock = Lock()
        self.cascade = cv.CascadeClassifier(model_file_path)

    def update(self,screenshot):
        self.lock.acquire()
        self.screenshot = screenshot
        self.lock.release()

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            if not self.screenshot is None:
                rectangles = self.cascade.detectMultiScale(self.screenshot)
                self.lock.acquire()
                self.rectangles = rectangles
                self.lock.release()