import cv2 as cv
import numpy as np
import math

class GestureDetect:
    def __init__(self, cap):
        self.cap = cap

        # self.lower_skin = np.array([15,20,70], dtype=np.uint8)
        # self.upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    def gesture_detect(self, hsv_skin):
        try:  # an error comes if it does not find anything in window as it cannot find contour of max area
            # therefore this try error statement
            ret, frame = self.cap.read()
            if not ret:
                pass

            frame = cv.flip(frame, 1)
            kernel = np.ones((3, 3), np.uint8)

                # define region of interest
            roi = frame[100:300, 100:300]

            cv.rectangle(frame, (100, 100), (300, 300), (0, 255, 0), 0)
            hsv = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

                # define range of skin color in HSV
            lower_skin = np.array(hsv_skin[0], dtype=np.uint8)
            upper_skin = np.array(hsv_skin[1], dtype=np.uint8)

                # extract skin colur imagw
            mask = cv.inRange(hsv, lower_skin, upper_skin)

                # extrapolate the hand to fill dark spots within
            mask = cv.dilate(mask, kernel, iterations=4)

                # blur the image
            mask = cv.GaussianBlur(mask, (5, 5), 100)

                # find contours
            contours, hierarchy = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            # print(contours)
            # print(hierarchy)
            # find contour of max area(hand)
            cnt = max(contours, key=lambda x: cv.contourArea(x))

            # approx the contour a little
            epsilon = 0.0005 * cv.arcLength(cnt, True)
            approx = cv.approxPolyDP(cnt, epsilon, True)

            # make convex hull around hand
            hull = cv.convexHull(cnt)

            # define area of hull and area of hand
            areahull = cv.contourArea(hull)
            areacnt = cv.contourArea(cnt)

                # find the percentage of area not covered by hand in convex hull
            arearatio = ((areahull - areacnt) / areacnt) * 100

                # find the defects in convex hull with respect to hand
            hull = cv.convexHull(approx, returnPoints=False)
            defects = cv.convexityDefects(approx, hull)

                # l = no. of defects
            l = 0

            # code for finding no. of defects due to fingers
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(approx[s][0])
                end = tuple(approx[e][0])
                far = tuple(approx[f][0])
                pt = (100, 180)

                    # find length of all sides of triangle
                a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                s = (a + b + c) / 2
                ar = math.sqrt(s * (s - a) * (s - b) * (s - c))

                    # distance between point and convex hull
                d = (2 * ar) / a

                    # apply cosine rule here
                angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57

                # ignore angles > 90 and ignore points very close to convex hull(they generally come due to noise)
                if angle <= 90 and d > 30:
                    l += 1
                    cv.circle(roi, far, 3, [255, 0, 0], -1)

                    # draw lines around hand
                cv.line(roi, start, end, [0, 255, 0], 2)

            l += 1

                # print corresponding gestures which are in their ranges
            font = cv.FONT_HERSHEY_SIMPLEX
            if l == 1:
                if areacnt < 2000:
                    cv.putText(frame, 'Put hand in the box', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
                else:
                    if arearatio < 12:
                        cv.putText(frame, '0', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
                    elif arearatio < 17.5:
                        cv.putText(frame, 'Best of luck', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)

                    else:
                        cv.putText(frame, '1', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)

            elif l == 2:
                cv.putText(frame, '2', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)

            elif l == 3:

                if arearatio < 27:
                    cv.putText(frame, '3', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)
                else:
                    cv.putText(frame, 'ok', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)

            elif l == 4:
                cv.putText(frame, '4', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)

            elif l == 5:
                cv.putText(frame, '5', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)

            elif l == 6:
                cv.putText(frame, 'reposition', (0, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)

            else:
                cv.putText(frame, 'reposition', (10, 50), font, 2, (0, 0, 255), 3, cv.LINE_AA)

            # show the windows

            # viewImage(frame, 'frame')
            # viewImage(mask, 'mask')

            cv.imshow('mask', mask)

            cv.imshow('frame', frame)
        except Exception:
            # traceback.print_exc()
            print('Настройте параметры hsv и поместите руку в прямоугольник')
            pass