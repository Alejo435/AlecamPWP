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
    gray_blur = cv2.blur(gray, (5, 5), 0)
    output = gray_blur.copy
    #shows image
    cv2.imshow(edge)

    key = cv2.waitKey(25)
    if key == ord("q"):
        break
    #To Do list:
    #Detect line edges
    #Use midpoint fromulat
    #Contour detection?? (?? == Look into)
cv2.destroyALLWindows()
source.release()



