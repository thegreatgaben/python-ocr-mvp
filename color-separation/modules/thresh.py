import cv2
import numpy as np
from skimage.filters import threshold_multiotsu
from modules.color import hsvMask


def otsu(img):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, th = cv2.threshold(grey, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th


def otsu_multiclass(grey, classes):
    thresholds = threshold_multiotsu(grey, classes)
    return thresholds.tolist()


def otsu_multiclass_grey(img, classes=2):
    grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresholds = otsu_multiclass(grey, classes)
    regions = np.digitize(grey, thresholds)
    regions = np.array(regions * 255, dtype=np.uint8)
    regions = cv2.equalizeHist(regions)
    return regions


def otsu_multiclass_rgb(img, classes=2):
    b, g, r = cv2.split(img)
    bgr = [b, g, r]
    for i in range(len(bgr)):
        thresholds = threshold_multiotsu(bgr[i], classes)
        regions = np.digitize(bgr[i], thresholds)
        regions = np.array(regions * 255, dtype=np.uint8)
        bgr[i] = cv2.equalizeHist(regions)
    return bgr


def otsu_multiclass_hsv(img, classes=2, threshold=True, hues=[(115, 25), (55, 25), (0, 25)], sat_range=(0, 255), val_range=(0, 255)):
    channels = []
    output_channels = []
    channel_metadata = []
    for hue in hues:
        # metadata handling
        metadata = {}
        metadata['hue'] = hue[0]
        metadata['hue_variance'] = hue[1]
        
        # start hsv masking
        channels.append(hsvMask(
            img,
            hue[0],
            hue[1],
            sat_range[0],
            sat_range[1],
            val_range[0],
            val_range[1],
        ))
        hsv = cv2.cvtColor(channels[-1], cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)

        # start thresholding
        if (threshold):
            try:
                thresholds = otsu_multiclass(s, classes)
            except:
                print('[otsu_multiclass_hsv]: skipped an image channel.')
                continue
            thresholded = np.digitize(s, thresholds)
            thresholded = np.array(thresholded * 255, dtype=np.uint8)
            equalized = cv2.equalizeHist(thresholded)
            output_channels.append(equalized)
            channel_metadata.append(metadata)
        else:
            output_channels.append(s)
            channel_metadata.append(metadata)
    return output_channels, channel_metadata
