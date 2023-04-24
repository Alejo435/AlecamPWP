import cv2
import numpy as np
import math
from numpy import ones,vstack
from numpy.linalg import lstsq
import matplotlib.pyplot as plt


source = cv2.VideoCapture('vroom.mp4')

while True:
    #detects image
    ret, img = source.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(onegray, 300, 400, apertureSize=3)
    lines = cv2.HoughLines(edges, 0.6, np.pi / 180, 200)

    pointvalues = {}
    line = {}
    xproduct = 0
    xproductr = 0

    #Detects line edges:
    for r_theta in lines:
        arr = np.array(r_theta[0], dtype=np.float64)
        r, theta = arr
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * r
        y0 = b * r
        x1 = int(x0 + 3500 * (-b))
        y1 = int(y0 + 3500 * (a))
        x2 = int(x0 - 4000 * (-b))
        y2 = int(y0 - 4000 * (a))

        # finds slope
        slope = [(x1, x1), (x2, y2)]
        x, y = zip(*slope)
        A = vstack([x, ones(len(x))]).T
        n, b = lstsq(A, y)[0]

        # calculates frst point
        fp = (0 - b) / n
        xproduct += fp

        # calculates second point
        sp = (5000 - b) / n
        xproductr += sp

        pointvalues[fp] = sp

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)

    i = 0
    slope = 0
    y_int = b
    for n, b in line:
        if i == 0:
            slope = n
            y_int = b


    #Determines length of line (Hence len)
    midfp = xproduct / len(pointvalues)
    midsp = xproductr / len(pointvalues)

    cv2.line(img, (int(midfp), 0), (int(midsp), 5000), (255, 0, 0), 5)

    key = cv2.waitKey(25)
    if key == ord("q"):
        break
    #To Do list:
    #Contour detection?? (?? == Look into)
cv2.destroyALLWindows()
source.release()



