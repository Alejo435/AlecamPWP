import cv2
import numpy as np
#from matplotlib import pyplot as plt

img = cv2.VideoCapture('IMG-1179.mp4')

while(True):
    #reads each frame
    ret, frame = img.read()
    #coverts image to grayscale and laods
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.blur(gray, (3, 3))

    output = frame.copy()
    circle = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, 1, 100000, param1 = 50, param2 = 30, minRadius = 100, maxRadius = 300)

    if circle is not None:
        circle = np.uint16(np.around(circle))

        for pt in circle[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            cv2.circle(output, (x,y), r, (0, 255, 0), 2)
            cv2.circle(output, (x,y), 1, (0, 0, 255), 3)
        cv2.imshow('frame',output)

    cv2.imshow("circle",output)
    if cv2.waitkey(25) == 0xFF == ord('w'):
        break

cv2.destroyALLWindows()