# import traceback
import cv2 as cv
import numpy as np
import math
from hsv import HSVSettings
from gdetect import GestureDetect

if __name__ == '__main__':
    # window settings
    cap = cv.VideoCapture(0)
    #cap.set(3, 1280)
    #cap.set(4, 720)

    get_hsv = HSVSettings(cap)
    gesture_detect = GestureDetect(cap)

    while(True):
        hsv = get_hsv.get_hsv()
        gesture_detect.gesture_detect(hsv)

        key = cv.waitKey(1)
        if key == 27:
            break
    cv.destroyAllWindows()