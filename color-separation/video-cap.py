import cv2
import numpy as np

cap = cv2.VideoCapture(0)

while True:
    _, frame = cap.read()

    blurred = cv2.blur(frame, (9, 9))
    edges = cv2.Canny(blurred, 30, 30)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100,
                            minLineLength=6, maxLineGap=8)
    # Draw lines on the image
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(edges, (x1, y1), (x2, y2), (255, 0, 0), 1)
    cv2.imshow("Live", edges)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
cap.release()
