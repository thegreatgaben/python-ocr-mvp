import cv2
import os
from skimage import io, img_as_float
import numpy as np


def viewImage(image, windowTitle="Display"):
    cv2.namedWindow(windowTitle, cv2.WINDOW_NORMAL)
    cv2.imshow('{}'.format(windowTitle), image)
    cv2.resizeWindow(windowTitle, 600, 600)
    cv2.waitKey()
    cv2.destroyAllWindows()


def getImageFileNames(path):
    file_list = []
    for filename in os.listdir(path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".bmp"):
            file_list.append(filename)
    return file_list


def averageIntensityValue(image):
    image = img_as_float(image)
    return np.mean(image)


def smartInvert(image):
    if (averageIntensityValue(image) >= 0.5):
        return (255 - image)
    else:
        return image
