import numpy as np
import cv2
from hsvMask import hsvMask


def nothing(val):
    pass


cap = cv2.VideoCapture(0)

while(True):
    cv2.namedWindow('frame')
    ret, frame = cap.read()
    cv2.createTrackbar('HSV', 'frame', 0, 180, nothing)
    j = cv2.getTrackbarPos('HSV', 'frame')
    result = hsvMask(frame, j)
    cv2.imshow('frame', result)
    if cv2.waitKey(3) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
