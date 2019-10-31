import cv2
import math
import numpy as np


def hsvMask(image, hue, var=15, sat_lo=80, sat_hi=255, val_lo=20, val_hi=255):
    assert (var < 90), "hue variance cannot be larger than 90!"
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hue_wrap = 0
    if (hue - var < 0 or hue + var > 180):
        if (hue - var < 0):
            hue_wrap = var - hue
            mask1_lo = np.array([hue - var + hue_wrap, sat_lo, val_lo])
            mask1_hi = np.array([hue + var, sat_hi, val_hi])
            mask2_lo = np.array([180 - hue_wrap, sat_lo, val_lo])
            mask2_hi = np.array([180, sat_hi, val_hi])
        elif (hue + var > 180):
            hue_wrap = hue + var - 180
            mask1_lo = np.array([hue - var, sat_lo, val_lo])
            mask1_hi = np.array([180, sat_hi, val_hi])
            mask2_lo = np.array([0, sat_lo, val_lo])
            mask2_hi = np.array([hue_wrap, sat_hi, val_hi])
        mask1 = cv2.inRange(hsv_img, mask1_lo, mask1_hi)
        mask2 = cv2.inRange(hsv_img, mask2_lo, mask2_hi)
        curr_mask = cv2.add(mask1, mask2)
    else:
        mask_lo = np.array([hue - var, sat_lo, val_lo])
        mask_hi = np.array([hue + var, sat_hi, val_hi])
        curr_mask = cv2.inRange(hsv_img, mask_lo, mask_hi)
    masked_img = cv2.bitwise_and(hsv_img, hsv_img, mask=curr_mask)
    rgb_img = cv2.cvtColor(masked_img, cv2.COLOR_HSV2BGR)
    return rgb_img


def apply_mask(matrix, mask, fill_value):
    masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
    return masked.filled()


def apply_threshold(matrix, low_value, high_value):
    low_mask = matrix < low_value
    matrix = apply_mask(matrix, low_mask, low_value)
    high_mask = matrix > high_value
    matrix = apply_mask(matrix, high_mask, high_value)

    return matrix


def simpleColorBalance(img, percent=1):
    assert img.shape[2] == 3
    assert percent > 0 and percent < 100
    half_percent = percent / 200.0
    channels = cv2.split(img)
    out_channels = []
    for channel in channels:
        assert len(channel.shape) == 2
        height, width = channel.shape
        vec_size = width * height
        flat = channel.reshape(vec_size)
        assert len(flat.shape) == 1
        flat = np.sort(flat)
        n_cols = flat.shape[0]
        low_val = flat[math.floor(n_cols * half_percent)]
        high_val = flat[math.ceil(n_cols * (1.0 - half_percent))]
        thresholded = apply_threshold(channel, low_val, high_val)
        normalized = cv2.normalize(
            thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
        out_channels.append(normalized)
    return cv2.merge(out_channels)


def invert(image):
    return (255-image)

def makeTransparent(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _,alpha = cv2.threshold(gray,0,255,cv2.THRESH_BINARY)
    b, g, r = cv2.split(image)
    rgba = [b,g,r, alpha]
    return cv2.merge(rgba, 4)

def RGB2CMYK(rgb, arrayInsteadOfTuple=False):
    r_ = rgb[0]/255
    g_ = rgb[1]/255
    b_ = rgb[2]/255
    k = 1 - max(r_, g_, b_)
    if float(k) == 1.0:
        return (0, 0, 0, 100)
    c = round((max(1 - r_ - k, 0) / (1 - k)) * 100)
    m = round((max(1 - g_ - k, 0) / (1 - k)) * 100)
    y = round((max(1 - b_ - k, 0) / (1 - k)) * 100)
    k = round(k * 100)
    if arrayInsteadOfTuple:
        return [c, m, y, k]
    return (c, m, y, k)


def CMYK2RGB(cmyk, arrayInsteadOfTuple=False):
    c = cmyk[0]
    m = cmyk[1]
    y = cmyk[2]
    k = cmyk[3]
    r = round(255 * (1 - (c / 100)) * (1 - (k / 100)))
    g = round(255 * (1 - (m / 100)) * (1 - (k / 100)))
    b = round(255 * (1 - (y / 100)) * (1 - (k / 100)))
    if arrayInsteadOfTuple:
        return [r, g, b]
    return (r, g, b)
