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


def splitHSVChannels(inputBGR):
    frame_HSV = cv2.cvtColor(inputBGR, cv2.COLOR_BGR2HSV)

    red = cv2.inRange(frame_HSV, (0, 130, 0), (60, 255, 255))
    yellow = cv2.inRange(frame_HSV, (61, 130, 0), (120, 255, 255))
    green = cv2.inRange(frame_HSV, (121, 130, 0), (180, 255, 255))
    cyan = cv2.inRange(frame_HSV, (181, 130, 0), (240, 255, 255))
    blue = cv2.inRange(frame_HSV, (241, 130, 0), (300, 255, 255))
    magenta = cv2.inRange(frame_HSV, (301, 130, 0), (360, 255, 255))

    return [red, yellow, green, cyan, blue, magenta]


def contourTest(image):
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    green_low = np.array([40, 60, 40])
    green_high = np.array([70, 255, 255])
    curr_mask = cv2.inRange(hsv_img, green_low, green_high)
    viewImage(curr_mask)
    masked = cv2.bitwise_and(hsv_img, hsv_img, mask=255 - curr_mask)
    viewImage(masked)


if __name__ == "__main__":
    print('hello openCV')
    inputBGR = cv2.imread('images/File 1.jpg')
    inputBGR = cv2.resize(inputBGR, (800, 800))
    inputBlurred = cv2.blur(inputBGR, (2, 2))

    # allSpacesHSV = splitHSVChannels(inputBGR)
    # for i in range(len(allSpacesHSV)):
    #     viewImage(allSpacesHSV[i], 'hsv')

    contourTest(inputBlurred)
    # out = contourTest(inputBGR)
    # viewImage(out)
