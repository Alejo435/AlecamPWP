import cv2
import numpy as np
#from matplotlib import pyplot as plt

img = cv2.VideoCapture('IMG-1179.mp4')

while(True):
    #reads each frame
    ret, frame = img.read()
    #coverts image to grayscale and adds frames to gray_blur
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.blur(gray, (3, 3))

    output = gray_blur.copy()
    #sets searching parameters for circle
    circle = cv2.HoughCircles(gray_blur, cv2.HOUGH_GRADIENT, 1, 100000, param1 = 50, param2 = 30, minRadius = 100, maxRadius = 300)

    #If the circle is detected with the set parameters, then the video will dislay with the detection circle outlining it
    if circle is not None:
        circle = np.uint16(np.around(circle))

        for pt in circle[0, :]:
            x, y, r = pt[0], pt[1], pt[2]
            cv2.circle(output, (x,y), r, (0, 255, 0), 2)
            cv2.circle(output, (x,y), 1, (0, 0, 255), 3)

        #displays video and should the user press w, the waitKey function, which checks for this every 25 miliseconds, will activate, cuasing the while loop to break and allowing the program to proceed with the destroyAllWindows function
        cv2.imshow("circle",output)
    if cv2.waitKey(25) & 0xFF == ord('w'):
        break
#destorys all remaining frames, cuasing video to close
cv2.destroyALLWindows()