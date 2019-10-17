import cv2
import numpy as np
from skimage.filters import threshold_multiotsu
# import hsvMask


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


# use corresponding channel's intensity for tresholding instead of greyscaled
def otsu_multi_rgb2(img, classes=2):
    b, g, r = cv2.split(img)
    bgr = [b, g, r]
    for i in range(len(bgr)):
        thresholds = threshold_multiotsu(bgr[i], classes)
        thresholds = thresholds.tolist()
        regions = np.digitize(bgr[i], thresholds)
        regions = np.array(regions * 255, dtype=np.uint8)
        bgr[i] = cv2.equalizeHist(regions)
    return bgr


def otsu_multi_hsv(img, classes=2, threshold=True):
    r = hsvMask(img, 0, 20, 0, 255, 0, 255)
    g = hsvMask(img, 55, 25, 0, 255, 0, 255)
    b = hsvMask(img, 115, 25, 0, 255, 0, 255)
    bgr = [b, g, r]
    for i in range(len(bgr)):
        hsv = cv2.cvtColor(bgr[i], cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        if (threshold):
            try:
                thresholds = threshold_multiotsu(s, classes)
            except:
                print(
                    'oops, [some image\'s channel {} has an error]'.format(i))
                continue
            thresholds = thresholds.tolist()
            regions = np.digitize(s, thresholds)
            regions = np.array(regions * 255, dtype=np.uint8)
            equalized = cv2.equalizeHist(regions)
            # kernel = cv2.getStructuringElement(
            #     shape=cv2.MORPH_ELLIPSE, ksize=(4, 4))
            # closed = cv2.morphologyEx(equalized, cv2.MORPH_CLOSE, kernel)
            # kernel = cv2.getStructuringElement(
            #     shape=cv2.MORPH_ELLIPSE, ksize=(2, 2))
            # closed = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
            # bgr[i] = closed
            bgr[i] = equalized
        else:
            bgr[i] = s
    zeroes = np.zeros(np.shape(bgr[0]), dtype=np.uint8)
    bgr[0] = cv2.merge((bgr[0], zeroes, zeroes))
    bgr[1] = cv2.merge((zeroes, bgr[1], zeroes))
    bgr[2] = cv2.merge((zeroes, zeroes, bgr[2]))
    return bgr


def hsvMask(image, hue_center, hue_var=15, sat_lo=80, sat_hi=255, val_lo=20, val_hi=255):
    # TODO: find optimal value for saturation and value
    assert (
        hue_var < 90), "hue variance cannot be larger than half of the hue spectrum (90)!"
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue_wrap = 0

    if (hue_center - hue_var < 0):
        hue_wrap = hue_var - hue_center
        mask1_lo = np.array([hue_center - hue_var + hue_wrap, sat_lo, val_lo])
        mask1_hi = np.array([hue_center + hue_var, sat_hi, val_hi])
        mask1 = cv2.inRange(hsv_img, mask1_lo, mask1_hi)
        mask2_lo = np.array([180 - hue_wrap, sat_lo, val_lo])
        mask2_hi = np.array([180, sat_hi, val_hi])
        mask2 = cv2.inRange(hsv_img, mask2_lo, mask2_hi)
        curr_mask = cv2.add(mask1, mask2)
    elif (hue_center + hue_var > 180):
        hue_wrap = hue_center + hue_var - 180
        mask1_lo = np.array([hue_center - hue_var, sat_lo, val_lo])
        mask1_hi = np.array([180, sat_hi, val_hi])
        mask1 = cv2.inRange(hsv_img, mask1_lo, mask1_hi)
        mask2_lo = np.array([0, sat_lo, val_lo])
        mask2_hi = np.array([hue_wrap, sat_hi, val_hi])
        mask2 = cv2.inRange(hsv_img, mask2_lo, mask2_hi)
        curr_mask = cv2.add(mask1, mask2)
    else:
        mask_lo = np.array([hue_center - hue_var, sat_lo, val_lo])
        mask_hi = np.array([hue_center + hue_var, sat_hi, val_hi])
        curr_mask = cv2.inRange(hsv_img, mask_lo, mask_hi)

    masked_img = cv2.bitwise_and(hsv_img, hsv_img, mask=curr_mask)
    rgb_img = cv2.cvtColor(masked_img, cv2.COLOR_HSV2BGR)
    return rgb_img
