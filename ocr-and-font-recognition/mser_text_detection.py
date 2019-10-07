from text_detection import TextDetection
from img_utils import *

import numpy as np
import cv2 as cv

class MSERTextDetection(TextDetection):

    def __init__(self, imagePath, minCoverageArea=0.01):
        TextDetection.__init__(self, imagePath);
        self.minCoverageArea = minCoverageArea;


    def detectTexts(self):
        mser = cv.MSER_create()

        # Preprocessing
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0);

        _, boxes = mser.detectRegions(blurred)
        mappedBoxes = [];
        for (x, y, w, h) in boxes:
            if w/self.imageWidth >= self.minCoverageArea and h/self.imageHeight >= self.minCoverageArea:
                mappedBoxes.append([x, y, x + w - 1, y + h - 1]);

        # Merge overlapping bounding boxes
        mappedBoxes = non_max_suppression_fast(np.array(mappedBoxes), overlapThresh=0.3);
        mappedBoxes = self.sortBoundingBoxes(mappedBoxes);
        mappedBoxes = self.mergeCloseBoundingBoxes(mappedBoxes);

        return mappedBoxes;


    def sortBoundingBoxes(self, boxes):
        '''
        Sorts bounding boxes from left to right and top to bottom
        '''
        # Sort boxes according to bottom-right y axis
        sortedBoxes = sorted(boxes, key=lambda rect: rect[-1]);
        lineBottom = sortedBoxes[0][-1];
        lineBegin = 0
        for i in range(len(sortedBoxes)):
            if sortedBoxes[i][1] > lineBottom:
                # Sort boxes according to bottom-right x axis
                sortedBoxes[lineBegin:i] = sorted(sortedBoxes[lineBegin:i], key=lambda rect: rect[-2])
                lineBegin = i
            lineBottom = max(sortedBoxes[i][-1], lineBottom)
        # sort the last line
        sortedBoxes[lineBegin:] = sorted(sortedBoxes[lineBegin:], key=lambda rect: rect[0])
        return sortedBoxes;


    def mergeCloseBoundingBoxes(self, sortedBoxes, proximityThresh=20):
        '''
        Merge bounding boxes that are in close proximity by some threshold.
        Only works for horizontal orientation at the moment
        '''
        mergedBoxes = [];
        rect = sortedBoxes[0];
        for i in range(len(sortedBoxes)-1):
            x1 = sortedBoxes[i][2];
            x2 = sortedBoxes[i+1][0];
            if abs(x1 - x2) <= proximityThresh:
                rect[0] = min([rect[0], sortedBoxes[i][0], x2]);
                rect[1] = min([rect[1], sortedBoxes[i][1], sortedBoxes[i+1][1]]);
                rect[2] = max([rect[2], x1, sortedBoxes[i+1][2]]);
                rect[3] = max([rect[3], sortedBoxes[i][3], sortedBoxes[i+1][3]]);
            else:
                mergedBoxes.append(rect);
                rect = sortedBoxes[i+1];

        return mergedBoxes;

