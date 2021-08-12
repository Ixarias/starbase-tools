import win32gui
import os

def winEnumHandler( hwnd, ctx ):
    if win32gui.IsWindowVisible( hwnd ):
        print (hwnd, win32gui.GetWindowText( hwnd ))

win32gui.EnumWindows( winEnumHandler, None )
print(os.getcwd())

# hwnd = win32gui.FindWindow(None, "Starbase")
# print(hwnd)
# win32gui.EnumChildWindows(hwnd, winEnumHandler, None)