import cv2
import numpy as np
import math
from numpy import ones,vstack
from numpy.linalg import lstsq
import matplotlib.pyplot as plt


source = cv2.VideoCapture('vroom3.mp4')


#applies 5 by 5 kernal window to imahge
def edges(img):
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   blur = cv2.GaussianBlur(gray, (5, 5), 0)
   edges = cv2.Canny(blur,  50, 150)
   return edges

#determines height of cropped area, gets required measuerments of the image of interst, and vreates an image that masks everything else
def crop(img):
    h = img.shape[0]
    poly = np.array([[(200, h), (1100, h), (550, 250)]])
    maskera = np.zeros_like(img)
    cv2.fillPoly(maskera, poly, 255)
    m_img = cv2.bitwise_and(img, maskera)
    return m_img

#getsother point from coresponding point, and specfies coodinates to mark slope and y intercept
def points(img, linesp):
    slope, intercepts = linesp
    y1 = img.shape[0]
    x1 = int((y1 - intercepts)/slope)
    y2 = int(y1*(3/5))
    x2 = int((y2 - intercepts)/slope)
    return np.array([x1, y1, x2, y2])

#Average of lines
def midline(img, lines):
    leftpoints = []
    rightpoints = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
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
            cv2.line(output, (x1, y1), (x2, y2), (0,255,0), 10)

    return output

while True:
   _, frame = source.read()
   can = edges(frame)
   ROI = crop(can)
   lines = cv2.HoughLinesP(ROI, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
   mid = midline(frame, lines)
   output = displayintime(frame, mid)
   midimg = cv2.addWeighted(frame, 0.8, output, 1, 1)
   cv2.imshow("The end is near", midimg)
   if cv2.waitKey(1) == ord('q'):
       break

cv2.destroyAllWindows()

#     pointvalues = {}
#     line = {}
#     xproduct = 0
#     xproductr = 0
#
#     #Detects line edges:
#     if lines is not None:
#         for r_theta in lines:
#             arr = np.array(r_theta[0], dtype=np.float64)
#             r, theta = arr
#             a = np.cos(theta)
#             b = np.sin(theta)
#             x0 = a * r
#             y0 = b * r
#             x1 = int(x0 + 3500 * (-b))
#             y1 = int(y0 + 3500 * (a))
#             x2 = int(x0 - 4000 * (-b))
#             y2 = int(y0 - 4000 * (a))
#
#             # finds slope
#             slope = [(x1, x1), (x2, y2)]
#             x, y = zip(*slope)
#             A = vstack([x, ones(len(x))]).T
#             n, b = lstsq(A, y)[0]
#
#             # calculates frst point
#             fp = (0 - b) / n
#             xproduct += fp
#
#             # calculates second point
#             sp = (5000 - b) / n
#             xproductr += sp
#
#             pointvalues[fp] = sp
#
#             cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
#
#         i = 0
#         slope = 0
#         y_int = b
#         for n, b in line:
#             if i == 0:
#                 slope = n
#                 y_int = b
#
#
#         #Determines length of line (Hence len)
#         midfp = xproduct / len(pointvalues)
#         midsp = xproductr / len(pointvalues)
#
#         cv2.line(img, (int(midfp), 0), (int(midsp), 5000), (255, 0, 0), 5)
#
#         cv2.imshow("detection_video", img)
#
#         key = cv2.waitKey(25)
#         if key == ord("q"):
#             break
#         #To Do list:
#         #Contour detection?? (?? == Look into)
