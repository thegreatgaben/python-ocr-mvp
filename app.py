import cv2
import numpy as np
import os
import math
import matplotlib


def viewImage(image, windowTitle="Display"):
    cv2.imshow('{}'.format(windowTitle), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print('Hello openCV')
    inputBGR = cv2.imread('color-separation-images/File 2.jpg')
    inputBGR = cv2.resize(inputBGR, (800, 800))
    viewImage(inputBGR, 'Image')
