import os
import numpy as np
from PIL import ImageGrab
import cv2
import time
import win32gui, win32api
import pytesseract
from pynput import keyboard
import copy

hwnd = win32gui.FindWindow(None, "Starbase")
win32gui.SetForegroundWindow(hwnd)
wr = win32gui.GetWindowRect(hwnd)

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
tess_config = r"--oem 1 --psm 3"

global screen

def on_activate_m():
  screenshot = copy.deepcopy(screen)
  gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
  _, threshold = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)
  contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  i = 0
  for contour in contours:
    # here we are ignoring first counter because 
    # findcontour function detects whole image as shape
    if i == 0:
        i = 1
        continue
  
    # cv2.approxPloyDP() function to approximate the shape
    approx = cv2.approxPolyDP(
        contour, 0.01 * cv2.arcLength(contour, True), True)
      
    if len(approx) == 4:
      if((approx[2][0][0]-approx[0][0][0])>100) and ((approx[2][0][1]-approx[1][0][1])>100):
        x, y = approx[0][0]
        h = approx[2][0][1]-y
        w = approx[1][0][0]-x
        crop = screenshot[y:y+h, x:x+w]
  # cv2.matchTemplate(screenshot, "structure.png", cv2.TM_CCOEFF_NORMED)
  data = pytesseract.image_to_data(crop, lang="eng", config=tess_config)
  print(data)
  item_name = ""
  for x,b in enumerate(data.splitlines()):
    if x!=0:
      b = b.split()
      if len(b)==12:
        if(b[2]=="1"):
          item_name += b[11]
        x,y,w,h = int(b[6]),int(b[7]),int(b[8]),int(b[9])
        # cv2.rectangle(crop, (x,y), (w+x, h+y), (0,0,255), 3)
        cv2.putText(crop, b[11], (x,y+25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (50,50,255), 2)
  cv2.imwrite(os.path.join(os.getcwd(), "sb_{}.png".format(item_name)), crop)
  print(data, file=open(os.path.join(os.getcwd(), "sb_{}.txt".format(item_name)), "a"))

last_time = time.time()
h = keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+m': on_activate_m})
h.start()
while(True):
  #screen = cv2.cvtColor(np.array(win32gui.FindWindow(None, "Starbase")), cv2.COLOR_BGRA2BGR)
  screen = cv2.cvtColor(np.array(ImageGrab.grab(bbox=(wr[0],wr[1],wr[2]-wr[0],wr[3]-wr[1]))), cv2.COLOR_RGB2BGR)
  # print("\033c", end="")
  # why broken >:()
  # cv2.imshow('sb_screen', screen)
  #  print('FPS {}'.format(1/(time.time()-last_time)))
  
  last_time=time.time()