import cv2
import numpy as np
from matplotlib import pyplot as plt


def histBackProj(src, bins=10, w=400, h=400):
    hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)
    ch = (0, 0)
    hue = np.empty(hsv.shape, hsv.dtype)
    cv2.mixChannels([hsv], [hue], ch)
    histSize = max(bins, 2)
    ranges = [0, 180]
    hist = cv2.calcHist([hue], [0], None, [histSize], ranges, accumulate=False)
    cv2.normalize(hist, hist, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    backproj = cv2.calcBackProject([hue], [0], hist, ranges, scale=1)

    bin_w = int(round(w / histSize))
    histImg = np.zeros((h, w, 3), dtype=np.uint8)

    for i in range(bins):
        cv2.rectangle(histImg, (i*bin_w, h), ((i+1)*bin_w, h -
                                              int(np.round(hist[i]*h/255.0))), (0, 0, 255), cv2.FILLED)

    return backproj, histImg


def equalizeSaturation(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    cv2.equalizeHist(h, h)
    hsv = cv2.merge((h, s, v))
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
    return bgr


def showRGBHistogram(img):
    col = ('b', 'g', 'r')
    for i in range(3):
        hist = cv2.calcHist([img], [i], None, [256], [0, 256])
        plt.plot(hist, color=col[i])
        plt.xlim([0, 256])
    plt.show()
