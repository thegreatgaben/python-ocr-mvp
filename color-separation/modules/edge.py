import cv2
import numpy as np


def cannyEdge(img, t1, t2, blur_size=1, line_thickness=1):
    img = cv2.blur(img, (blur_size, blur_size))
    edges = cv2.Canny(img, t1, t2)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                            minLineLength=6, maxLineGap=8)
    if (type(lines) == None):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(edges, (x1, y1), (x2, y2), (255, 0, 0), line_thickness)
    return edges
