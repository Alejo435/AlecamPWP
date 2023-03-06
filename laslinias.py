import cv2
import numpy as np
from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import ward, fcluster

# img = cv2.imread('IMG-1198.jpg')
#
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# edges = cv2.Canny(gray, 50, 150, apertureSize=3)
# lines = cv2.HoughLines(edges, 1, np.pi/ 180, 200)
#
# for r_theta in lines:
#     arr = np.array(r_theta[0], dtype=np.float64)
#     r, theta = arr
#     a = np.cos(theta)
#     b = np.sin(theta)
#     x0 = a * r
#     y0 = b * r
#     x1 = int(x0 + 1000 * (-b))
#     y1 = int(y0 + 1000 * (a))
#     x2 = int(x0 - 1000 * (-b))
#     y2 = int(y0 - 1000 * (a))
#     cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
#
# cv2.imwrite('linesDetected.jpg', img)

img = cv2.imread('IMG-1199.jpg')
img_canny = cv2.Canny(img, 50, 200, 3)

lines = cv2.HoughLines(img_canny, 1, 5* np.pi / 180, 150)

def find_parallel_lines(lines):

    lines_ = lines[:, 0, :]
    angle = lines_[:, 1]

    # Perform hierarchical clustering

    angle_ = angle[..., np.newaxis]
    y = pdist(angle_)
    Z = ward(y)
    cluster = fcluster(Z, 0.5, criterion='distance')

    parallel_lines = []
    for i in range(cluster.min(), cluster.max() + 1):
        temp = lines[np.where(cluster == i)]
        parallel_lines.append(temp.copy())

    return parallel_lines