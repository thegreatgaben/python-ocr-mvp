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


if __name__ == "__main__":
    print('hello openCV')
    inputBGR = cv2.imread('images/File 2.jpg')
    inputBGR = cv2.resize(inputBGR, (800, 800))

    allSpacesHSV = splitHSVChannels(inputBGR)

    for i in range(len(allSpacesHSV)):
        viewImage(allSpacesHSV[i], 'hsv')
