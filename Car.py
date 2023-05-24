import cv2
import numpy as np
import math
from numpy import ones,vstack
from numpy.linalg import lstsq

source = cv2.VideoCapture('vroom3.mp4')

pointvalues = {}
line = {}
xproduct = 0
xproductr = 0

#applies 5 by 5 kernal window to imahge
def edges(img):
    if img is not None:
       gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
       blur = cv2.GaussianBlur(gray, (5, 5), 0)
       edges = cv2.Canny(blur,  50, 150)
       return edges

#determines height of cropped area, gets required measuerments of the image of interst, and vreates an image that masks everything else
def crop(img):
    h = img.shape[0]
    #masks image
    poly = np.array([[(50, h), (1800, h), (800, 500), (650,500)]])
    maskera = np.zeros_like(img)
    cv2.fillPoly(maskera, poly, 255)
    m_img = cv2.bitwise_and(img, maskera)
    return m_img

#getsother point from coresponding point, and specfies coodinates to mark slope and y intercept
def points(img, linesp):
    try:
        slope, intercepts = linesp
    except TypeError:
        slope, intercepts = 0.001,0
    y1 = img.shape[0]
    # uses slope and y point to find x
    x1 = int((y1 - intercepts)/slope)
    y2 = int(y1*(3/5))
    x2 = int((y2 - intercepts)/slope)
    #Parameters to ensure nothing the array cant handle is appended
    if x1 <= 0:
        x1 = 100
    if x1 >= 100000:
        x1 = 1000
    if x2 <= 0:
        x2 = 100
    if x2 >= 1000000:
        x2 = 1000
    # print(x1)
    # print(x2)
    return np.array([x1, y1, x2, y2])

#Average of lines
def midline(img, lines):
    output = np.zeros_like(img)
    leftpoints = []
    rightpoints = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line.reshape(4)
            parameters = np.polyfit((x1, x2), (y1, y2), 1)
            slope = parameters[0]
            intercept = parameters[1]
            #So that lines are displayed seperately
            if slope < 0:
                leftpoints.append((slope, intercept))
            else:
                rightpoints.append((slope, intercept))
        leftpoints_average = np.average(leftpoints, axis=0)
        rightpoints_average = np.average(rightpoints, axis=0)
        lline = points(img, leftpoints_average)
        rline = points(img, rightpoints_average)
        return np.array([lline, rline])

def displayintime(img, lines):
    output = np.zeros_like(img)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(output, (int(x1), int(y1)), (int(x2), int(y2)), (0,255,0), 10)

    return output

def midlines(img, lines, xproduct, xproductr, mid):
    output2 = np.zeros_like(img)
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            sl = [(x1, x1), (x2, y2)]
            x, y = zip(*sl)
            A = vstack([x, ones(len(x))]).T
            n, b = lstsq(A, y)[0]

            # calculates frst point
            fp = (0 - b) / n
            xproduct += fp

            # calculates second point
            sp = (5000 - b) / n
            xproductr += sp

            pointvalues[fp] = sp

        midfp = xproduct / len(pointvalues)
        midsp = xproductr / len(pointvalues)
        print(midfp)
        print(midsp)

        cv2.line(output2, (int(midfp), 0), (int(midsp), 5000), (255, 0, 0), 5)

    return output2


while True:
   _, frame = source.read()
   can = edges(frame)
   ROI = crop(can)
   lines = cv2.HoughLinesP(ROI, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
   mid = midline(frame, lines)
   output = displayintime(frame, mid)
   midimg = cv2.addWeighted(frame, 0.8, output, 1, 1)
   output2 = midlines(frame, mid, xproduct, xproductr, lines)
   midimg2 = cv2.addWeighted(frame, 0.8, output, 1, 1)
   cv2.imshow("The end is near", midimg2)
   if cv2.waitKey(1) == ord('q'):
       break

cv2.destroyAllWindows()

