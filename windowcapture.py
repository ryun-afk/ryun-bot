import numpy as np
import win32gui, win32ui, win32con, win32api

class WindowCapture:

    width = 0
    height = 0
    hwnd = None


    def __init__(self, window_name):
    
        self.width = win32api.GetSystemMetrics(0)
        self.height = win32api.GetSystemMetrics(1)
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not foundL: {}'.format(window_name))

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