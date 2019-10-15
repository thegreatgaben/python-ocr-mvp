import cv2
import os


def viewImage(image, windowTitle="Display"):
    cv2.imshow('{}'.format(windowTitle), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def getImageFileNames(path):
    file_list = []
    for filename in os.listdir(path):
        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".bmp"):
            file_list.append(filename)
    return file_list
