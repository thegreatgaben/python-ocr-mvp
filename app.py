import cv2
import numpy as np
import os, math

def viewImage(image):
  cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
  cv2.imshow('Image', image)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

def getImagePaths(folderName):
  images = []
  for filename in os.listdir(folderName):
    if filename.endswith(".jpg") or filename.endswith(".png"):
      images.append(folderName + '/' + filename)
  return images

if __name__ == "__main__":
  print('hello openCV')