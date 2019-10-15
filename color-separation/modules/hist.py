import cv2 as cv
import numpy as np


def histBackProj(src, bins=10, w=400, h=400):
    hsv = cv.cvtColor(src, cv.COLOR_BGR2HSV)
    ch = (0, 0)
    hue = np.empty(hsv.shape, hsv.dtype)
    cv.mixChannels([hsv], [hue], ch)
    histSize = max(bins, 2)
    ranges = [0, 180]
    hist = cv.calcHist([hue], [0], None, [histSize], ranges, accumulate=False)
    cv.normalize(hist, hist, alpha=0, beta=255, norm_type=cv.NORM_MINMAX)
    backproj = cv.calcBackProject([hue], [0], hist, ranges, scale=1)

    bin_w = int(round(w / histSize))
    histImg = np.zeros((h, w, 3), dtype=np.uint8)

    for i in range(bins):
        cv.rectangle(histImg, (i*bin_w, h), ((i+1)*bin_w, h -
                                             int(np.round(hist[i]*h/255.0))), (0, 0, 255), cv.FILLED)

    return backproj, histImg
