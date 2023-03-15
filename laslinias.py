import cv2
import numpy as np


img = cv2.imread('IMG-4654 (1).jpg')

onegray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(onegray, 300, 400, apertureSize=3)
lines = cv2.HoughLines(edges, 0.9, np.pi/ 180, 200)

far = []
sum = 0

for r_theta in lines:
    arr = np.array(r_theta[0], dtype=np.float64)
    r, theta = arr
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * r
    y0 = b * r
    x1 = int(x0 + 10000000 * (-b))
    y1 = int(y0 + 10000000 * (a))
    x2 = int(x0 - 10000000 * (-b))
    y2 = int(y0 - 10000000 * (a))
    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 5)

#mid = int(sum/len(far))
#mid = cv2.line(img, (mid, 180), (mid, 1000), (0, 0, 255), 2)

cv2.imwrite('linesDetected.jpg', img)

