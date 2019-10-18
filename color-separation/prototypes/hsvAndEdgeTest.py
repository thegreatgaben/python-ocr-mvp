import cv2
import numpy as np
import math
import matplotlib
from hsvMask import hsvMask
from edgeDetect import edgeDetect


def nothing(x):
    pass


if __name__ == "__main__":

    hue = 0
    while True:
        cv2.namedWindow('frame')
        frame = cv2.imread('images/img1.jpg')
        frame = cv2.resize(frame, (1000, 700))
        cv2.createTrackbar('t1', 'frame', 20, 200, nothing)
        cv2.createTrackbar('t2', 'frame', 40, 200, nothing)
        t1 = cv2.getTrackbarPos('t1', 'frame')
        t2 = cv2.getTrackbarPos('t2', 'frame')
        edges = edgeDetect(frame, t1, t2, 10)
        hue_masked = hsvMask(frame, hue)
        edges = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        combined = cv2.addWeighted(hue_masked, 0.8, edges, 1, 0)
        cv2.imshow('frame', combined)
        k = cv2.waitKey(5) & 0xFF
        hue += 3
        if hue >= 180:
            hue = 0
        if k == 27:
            break
    cv2.destroyAllWindows()
    cap.release()
