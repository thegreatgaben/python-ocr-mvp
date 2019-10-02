import cv2
import numpy as np
import os
import math
import matplotlib


def viewImage(image, windowTitle="Display"):
    cv2.imshow('{}'.format(windowTitle), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def hsvMask(image, hue_center, hue_var=15, sat_lo=70, sat_hi=255, val_lo=20, val_hi=255):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    assert (hue_var <
            90), "hue variance cannot be larger than half of the hue spectrum (90)!"

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


if __name__ == "__main__":
    print('starting color separation')
    # only testing on one image at the moment
    inputBGR = cv2.imread('images/File 10.png')
    inputBGR = cv2.resize(inputBGR, (1600, 1600))
    for h in range(0, 180, 10):  # hue channel
        for i in range(1, 6):  # structuring element diameter
            blurred = cv2.blur(inputBGR, (25, 25))
            masked = hsvMask(blurred, h)
            strel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (i, i))
            opened = cv2.morphologyEx(masked, cv2.MORPH_DILATE, strel)
            cv2.imwrite("outputs/{}-{}.bmp".format(h, i), opened)
    print('ouptut written')
