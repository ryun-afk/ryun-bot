import numpy as np
import win32gui, win32ui, win32con
from threading import Thread, Lock


class WindowCapture:
    # threading properties
    stopped = True
    lock = None
    screenshot = None
    # properties
    width = 0
    height = 0
    hwnd = None
    cropped_left = 0
    cropper_right = 0
    cropped_top = 0
    cropped_bottom = 0


    def __init__(self, window_name = None):
        self.lock = Lock()

        # find target window, else use entire primary screen 
        if window_name is None:
            self.hwnd = win32gui.GetActiveWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
            
        
        # get window size
        window_size = win32gui.GetWindowRect(self.hwnd)
        self.width = window_size[2] - window_size[0]
        self.height = window_size[3] - window_size[1]

        # trimming window sides
        self.cropped_left = 0
        self.cropped_right = 0
        self.cropped_top = 0
        self.cropped_bottom = 0

        # adjusting resized window
        self.width = self.width - self.cropped_left - self.cropped_right
        self.height = self.height - self.cropped_top - self.cropped_bottom
        self.offset_x = window_size[0] + self.cropped_left
        self.offset_y = window_size[1] + self.cropped_top


    def get_screenshot(self):
        
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj,self.width,self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.width,self.height),dcObj,(0,0),win32con.SRCCOPY)

        #dataBitMap.SaveBitmapFile(cDC,'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray,dtype='uint8')
        img.shape = (self.height,self.width,4)


        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd,wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        # removes alpha channel to avoid cv.matchTemplate() error
        img = img[...,:3]

        # make image C_CONTIGUOUS to avoid errors with draw_rectangles
        img = np.ascontiguousarray(img)

        return img
    

    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd,ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd),win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler,None)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)
    
    # threading methods
    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        # TODO: you can write your own time/iterations calculation to determine how fast this is
        while not self.stopped:
            # get an updated image of the game
            screenshot = self.get_screenshot()
            # lock the thread while updating the results
            self.lock.acquire()
            self.screenshot = screenshot
            self.lock.release()