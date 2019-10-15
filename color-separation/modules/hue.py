import cv2
import numpy as np


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

