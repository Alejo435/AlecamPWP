import cv2
import numpy as np

source = cv2.VideoCapture('vroom.mp4')

def edges(img):
   gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
   blur = cv2.GaussianBlur(gray, (5, 5), 0)
   edges = cv2.Canny(blur,  50, 150)
   return edges


def crop(img):
    h = img.shape[0]
    poly = np.array([[(50, h), (1400, h), (800, 250)]])
    maskera = np.zeros_like(img)
    cv2.fillPoly(maskera, poly, 255)
    m_img = cv2.bitwise_and(img, maskera)
    return m_img

while True:
   _, frame = source.read()
   can = edges(frame)
   ROI = crop(can)
   cv2.imshow("The end is near", ROI)
   lines = cv2.HoughLinesP(ROI, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap=5)
   if cv2.waitKey(1) == ord('q'):
       break