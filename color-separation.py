import cv2
import numpy as np
import os
import math
import matplotlib


def viewImage(image, windowTitle="Display"):
    cv2.imshow('{}'.format(windowTitle), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getImagePaths(folderName):
    images = []
    for filename in os.listdir(folderName):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            images.append(folderName + '/' + filename)
    return images


def hsvMask(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    mask1_low = np.array([160, 150, 40])
    mask1_high = np.array([180, 255, 255])
    curr_mask = cv2.inRange(hsv_img, mask1_low, mask1_high)

    mask2_low = np.array([0, 150, 40])
    mask2_high = np.array([10, 255, 255])
    curr_mask2 = cv2.inRange(hsv_img, mask2_low, mask2_high)

    curr_mask = cv2.add(curr_mask, curr_mask2)
    masked_img = cv2.bitwise_and(hsv_img, hsv_img, mask=curr_mask)
    rgb_img = cv2.cvtColor(masked_img, cv2.COLOR_HSV2BGR)
    return rgb_img


if __name__ == "__main__":
    print('starting color-separation')
    inputBGR = cv2.imread('color-separation-images/File 1.jpg')
    inputBGR = cv2.resize(inputBGR, (1600, 1600))
    for i in range(1, 11):
        blurred = cv2.blur(inputBGR, (1, 1))
        masked = hsvMask(blurred)
        strel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (i, i))
        opened = cv2.morphologyEx(masked, cv2.MORPH_OPEN, strel)
        cv2.imwrite("color-separation-outputs/{}.bmp".format(i), opened)
    print('ouptut written')
