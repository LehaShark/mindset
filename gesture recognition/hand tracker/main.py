import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm



if __name__ == '__main__':
    import cv2
    import mediapipe as mp

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands

    # For webcam input:
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()

    # cap = cv2.VideoCapture(0)
    #
    # mpHands = mp.solutions.hands
    # hands = mpHands.Hands(False)
    # mpDraw = mp.solutions.drawing_utils
    #
    # while(True):
    #     success, img = cap.read()
    #     imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #     results = hands.process(imgRGB)
    #     if results.multi_hand_landmarks:
    #         for handLms in results.multi_hand_landmarks:
    #             mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    #
    #     cv2.imshow('Im', img)
    #     cv2.waitKey(1)


    ###################### For class
    # pTime = 0
    # cTime = 0
    # cap = cv2.VideoCapture(0)
    # detector = htm.handDetector()
    # while True:
    #     success, img = cap.read()
    #     img = detector.findHands(img)
    #     lmList = detector.findPosition(img)
    #     if len(lmList) != 0:
    #         print(lmList[4])
    #
    #     cTime = time.time()
    #     fps = 1 / (cTime - pTime)
    #     pTime = cTime
    #
    #     cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
    #                 (255, 0, 255), 3)
    #
    #     cv2.imshow("Image", img)
    #     cv2.waitKey(1)


# For counter
    # wCam, hCam = 640, 480
    # cap = cv2.VideoCapture(1)
    # cap.set(3, wCam)
    # cap.set(4, hCam)
    # while True:
    #     success, img = cap.read()
    #     cv2.imshow("Image", img)
    #     cv2.waitKey(1)
