import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:

    hwnd = None
    width = 0
    height = 0


    def __init__(self, window_name = None):
    
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            self.hwnd = win32gui.GetDesktopWindow()
            
        
        window_size = win32gui.GetWindowRect(self.hwnd)
        self.width = window_size[2] - window_size[0]
        self.height = window_size[3] - window_size[1]

        #self.width = int(self.width/2)
        #self.height = int(self.height/2)


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