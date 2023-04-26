import cv2
import numpy as np
import math
from numpy import ones,vstack
from numpy.linalg import lstsq
import matplotlib.pyplot as plt
source = cv2.VideoCapture('vroom2.mp4')

while True:
    ret, img = source.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,150,200,apertureSize = 3)

    minLineLength = 0
    maxLineGap = 400
    parallelism =[]
    lines = cv2.HoughLinesP(edges, rho=1 , theta= np.pi/180, threshold = 60, minLineLength=0, maxLineGap=400)
    a = np.array(lines)

    if lines is not None:
        #Checks for extra lines to ensure only parallels remain, does this by checking for repeating and unparallelled lines within a circle
        for x in range(len(lines)):
            for y in range(x+1, len(lines)):
                line1 = lines[x][0]
                line2 = lines[y][0]
                ang = np.arctan2(line1[1]-line1[3], line1[0]-line1[2]) * 180 / np.pi
                ang2 = np.arctan2(line2[1]-line2[3], line2[0]-line2[2]) * 180 / np.pi
                if np.abs(ang - ang2) < 5:
                    parallelism.append((line1, line2))

        #essentially midpoint formula, finds the 4 points on the center line to draw it
        def drawing(x1, y1, x2, y2, color, chungus):
            close = False
            for extras in parallelism:
                #Draws cicrcle to check intercection on borders
                if (abs(extras[0][0]-x1) < 100 and abs(extras[0][1] -y1) < 100) or (abs(extras[0][2]-x2) <100 and abs(extras[0][3] -y2) < 100):
                    close = True
                    break
            if close:
                color = (0,255, 0)
            cv2.line(img, (x1, y1), (x2, y2), color, chungus)

        #Function will display the detected lines in image, in this case only midpoint
        for puntos in parallelism:
            drawing(int((puntos[0][0] + puntos[1][0])/2), int((puntos[0][1]+puntos[1][1])/2), int((puntos[0][2]+ puntos[1][2])/2), int((puntos[0][3]+puntos[1][3])/2),(0, 0, 255), 2)

        key = cv2.waitKey(25)
        if key == ord("q"):
            break


cv2.destroyALLWindows()
