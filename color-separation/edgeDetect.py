# Video capture test for canny edge detector and edge linking using hough transform.
import cv2
import numpy as np


def edgeDetect(img, t1, t2):
    blurred = cv2.blur(img, (9, 9))
    edges = cv2.Canny(blurred, t1, t2)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                            minLineLength=6, maxLineGap=8)
    if (type(lines) == None):
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(edges, (x1, y1), (x2, y2), (255, 0, 0), 1)
    return edges


def nothing(x):
    pass


if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    while True:
        cv2.namedWindow('frame')
        _, frame = cap.read()
        cv2.createTrackbar('t1', 'frame', 0, 200, nothing)
        cv2.createTrackbar('t2', 'frame', 0, 200, nothing)
        t1 = cv2.getTrackbarPos('t1', 'frame')
        t2 = cv2.getTrackbarPos('t2', 'frame')
        frame = edgeDetect(frame, 20, 40)
        cv2.imshow('frame', frame)
        k = cv2.waitKey(5) & 0xFF
        if k == 27:
            break
    cv2.destroyAllWindows()
    cap.release()
