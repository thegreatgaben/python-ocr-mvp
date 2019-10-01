import cv2
import numpy as np
import os, math

def gridShow(images):
  rowLength = math.ceil(math.sqrt(len(images)))
  print('{} images, rowlength = {}'.format(len(images), rowLength))
  gridAccumulator = ()
  k = 0
  thisRow = ()
  for i in range(len(images)):
    thisRow = thisRow + (images[i],)
    k += 1
    if (i == len(images)-1): 
      while (len(thisRow) < rowLength):
        thisRow = thisRow + (images[i],)
    if (k >= rowLength):
      thisRow = np.column_stack(thisRow)
      gridAccumulator = gridAccumulator + (thisRow,)
      k = 0
      thisRow = ()
  return np.column_stack(gridAccumulator)