import numpy as np
import cv2 as cv

class HSVSettings:
    def __init__(self, cap):
        self.cap = cap

        cv.namedWindow("Trackbars")

        cv.createTrackbar("L - H", "Trackbars", 0, 179, lambda:None)
        cv.createTrackbar("L - S", "Trackbars", 0, 255, lambda:None)
        cv.createTrackbar("L - V", "Trackbars", 0, 255, lambda:None)
        cv.createTrackbar("U - H", "Trackbars", 179, 179, lambda:None)
        cv.createTrackbar("U - S", "Trackbars", 255, 255, lambda:None)
        cv.createTrackbar("U - V", "Trackbars", 255, 255, lambda:None)

    def get_hsv(self):
        # Start reading the webcam feed frame by frame.
        ret, frame = self.cap.read()
        if not ret:
            pass
        # Flip the frame horizontally (Not required)
        frame = cv.flip(frame, 1)

        # Convert the BGR image to HSV image.
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        # Get the new values of the trackbar in real time as the user changes
        # them
        l_h = cv.getTrackbarPos("L - H", "Trackbars")
        l_s = cv.getTrackbarPos("L - S", "Trackbars")
        l_v = cv.getTrackbarPos("L - V", "Trackbars")
        u_h = cv.getTrackbarPos("U - H", "Trackbars")
        u_s = cv.getTrackbarPos("U - S", "Trackbars")
        u_v = cv.getTrackbarPos("U - V", "Trackbars")

        # Set the lower and upper HSV range according to the value selected
        # by the trackbar
        lower_range = np.array([l_h, l_s, l_v])
        upper_range = np.array([u_h, u_s, u_v])

        # Filter the image and get the binary mask, where white represents
        # your target color
        mask = cv.inRange(hsv, lower_range, upper_range)

        # You can also visualize the real part of the target color (Optional)
        res = cv.bitwise_and(frame, frame, mask=mask)

        # Converting the binary mask to 3 channel image, this is just so
        # we can stack it with the others
        mask_3 = cv.cvtColor(mask, cv.COLOR_GRAY2BGR)

        # stack the mask, orginal frame and the filtered result
        stacked = np.hstack((mask_3, frame, res))

        # Show this stacked frame at 40% of the size.
        cv.imshow('Trackbars', cv.resize(stacked, None, fx=0.4, fy=0.4))

        hsv = [[l_h, l_s, l_v], [u_h, u_s, u_v]]

        # print(hsv)

        return hsv