import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('IMG-1179.mp4')

#coverts image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray_blur = cv2.blur(gray, (3, 3))

# output = img.copy()
# circle = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 1.3, 100)
#
# if circle is not None:
#     circle = np.round(circle[0, :]).astype("int")
#     print(circle)
#     for (x, y, r) in circle:
#         cv2.circle(output, (x,y), r, (0, 255, 0), 2)
#
# cv2.imshow("circle",output)
# cv2.waitkey(0)