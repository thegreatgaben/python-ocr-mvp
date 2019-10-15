import cv2
import numpy as np
from skimage.filters import threshold_multiotsu


def otsu(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th


def otsu_multi_grey(img, classes=2):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholds = threshold_multiotsu(grey, classes)
    thresholds = thresholds.tolist()
    regions = np.digitize(grey, thresholds)
    regions = np.array(regions * 255, dtype=np.uint8)
    regions = cv2.equalizeHist(regions)
    return regions


def otsu_multi_rgb(img, classes=2):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholds = threshold_multiotsu(grey, classes)
    thresholds = thresholds.tolist()
    regions = np.digitize(img, thresholds)
    b, g, r = cv2.split(regions)
    bgr = [b, g, r]
    for i in range(len(bgr)):
      bgr[i] = np.array(bgr[i] * 255, dtype=np.uint8)
      bgr[i] = cv2.equalizeHist(bgr[i])
    return bgr
