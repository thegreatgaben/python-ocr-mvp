from text_detection import TextDetection
from swt import SWTScrubber
import img_utils

import os
import numpy as np
import cv2 as cv

def nothing(x):
    pass;

class MSERTextDetection(TextDetection):

    def __init__(self, imagePath):
        TextDetection.__init__(self, imagePath);


    def detectTexts(self):
        mser = cv.MSER_create()

        # Preprocessing
        gray = cv.cvtColor(self.image, cv.COLOR_BGR2GRAY)
        blurred = cv.GaussianBlur(gray, (5, 5), 0);

        _, boxes = mser.detectRegions(blurred)

        mappedBoxes = [];
        for (x, y, w, h) in boxes:
            mappedBoxes.append([x, y, x + w - 1, y + h - 1]);

        # Merge overlapping bounding boxes
        mappedBoxes = img_utils.non_max_suppression_fast(np.array(mappedBoxes), overlapThresh=0.3);

        # MSER may only detect characters as regions instead of a text line
        mappedBoxes = self.sortBoundingBoxes(mappedBoxes);
        mappedBoxes = self.mergeCloseBoundingBoxes(mappedBoxes);

        # May have overlapping regions again
        mappedBoxes = img_utils.non_max_suppression_fast(np.array(mappedBoxes), overlapThresh=0.3);

        finalBoxes = self.filterBoundingBoxes(blurred, mappedBoxes);

        vis = self.drawTextRegions(finalBoxes);
        filename = 'mser_detected_texts.{}'.format(self.imageExt);
        img_utils.outputImage(vis, filename);

        return finalBoxes;


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


    def filterBoundingBoxes(self, preprocessed, boxes):
        filteredBoxes = [];
        swt = SWTScrubber();
        (edges, sobelx, sobely, theta) = swt.create_derivative(preprocessed);

        for (x1, y1, x2, y2) in boxes:
            w = abs(x1 - x2) + 1;
            h = abs(y1 - y2) + 1;

            if w/self.imageWidth < 0.01 or h/self.imageHeight < 0.01:
                continue;

            aspectRatio = w/h;
            if aspectRatio < 0.4 or aspectRatio > 20.0:
                continue;

            (textSWT, componentsMap) = swt.scrubWithDerivative(
                    edges[y1:y2, x1:x2],
                    sobelx[y1:y2, x1:x2],
                    sobely[y1:y2, x1:x2],
                    theta[y1:y2, x1:x2]
            );
            variances = [];
            for label,component in componentsMap.items():
                swtVariance = np.var(textSWT[np.nonzero(component)]);
                if swtVariance > 0:
                    variances.append(swtVariance);

            if len(variances) == 0:
                continue;

            meanVariance = np.mean(np.array(variances));
            print("Mean variance: {}".format(meanVariance));
            '''
            cv.imshow('image', textSWT);
            cv.waitKey(0);
            '''
            if meanVariance < 1.0 or meanVariance > 40.0:
                continue;

            filteredBoxes.append([x1, y1, x2, y2]);

        return filteredBoxes;

