# future plans to learn arduino and replace controls

from time import sleep
import win32gui, win32ui,win32con

class Control:
    FOWARD = 0x57
    LEFT = 0x41
    DOWN = 0x53
    RIGHT = 0x44

    window_name = "Mabinogi"


def main(window_name):
    hwnd = win32gui.FindWindow(None,window_name)
    win32gui.SetForegroundWindow(hwnd)
    sleep(4)

    win32gui.SendMessage(hwnd,win32con.WM_KEYDOWN,0x57,0)
    sleep(10)
    win32gui.SendMessage(hwnd,win32con.WM_KEYUP,0x57,0)


def get_inner_windows(whndl):
    def callback(hwnd,hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            hwnds[win32gui.GetClassName(hwnd)] = hwnd
        return True
    hwnds = {}
    win32gui.EnumChildWindows(whndl,callback,hwnds)
    return hwnds

def list_window_names():
    def winEnumHandler(hwnd,ctx):
        if win32gui.IsWindowVisible(hwnd):
            print(hex(hwnd),'"'+win32gui.GetWindowText(hwnd)+'"')
    win32gui.EnumWindows(winEnumHandler,None)

def list_inner_windows(window_name):
    whndl = win32gui.FindWindow(None,window_name)
    def callback(hwnd,hwnds):
        if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
            hwnds[win32gui.GetClassName(hwnd)] = hwnd
        return True
    hwnds = {}
    win32gui.EnumChildWindows(whndl,callback,hwnds)
    print(hwnds)

# for getting all windows
def find_all_windows(name):
    result = []
    def winEnumHandler(hwnd,ctx):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) == name:
            result.append(hwnd)
    win32gui.EnumWindows(winEnumHandler,None)
    return result


main("Mabinogi")
#list_window_names()

