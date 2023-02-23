import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('IMG_1099.MOV')

#coverts image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
