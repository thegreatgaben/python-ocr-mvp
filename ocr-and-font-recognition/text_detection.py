'''
Based on this tutorial here:
https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
'''

from img_utils import *

from imutils.object_detection import non_max_suppression
import math
import numpy as np
import time
import os
import cv2 as cv

class TextDetection:

    def __init__(self, imagePath, minConfidence):
        self.minConfidence = minConfidence;
        self.mainDir = os.path.dirname(__file__)

        # load the input image and grab the image dimensions
        self.imageName = os.path.basename(imagePath);
        self.image = cv.imread(imagePath)
        self.origImage = self.image.copy()
        (self.imageHeight, self.imageWidth) = self.image.shape[:2]

        # set the new width and height and then determine the ratio in change
        # for both the width and height
        # NOTE: The EAST text detector only accepts image with dimensions of multiples of 32
        (newW, newH) = (math.ceil(self.imageWidth/32) * 32, math.ceil(self.imageHeight/32) * 32)
        self.ratioW = self.imageWidth / float(newW)
        self.ratioH = self.imageHeight / float(newH)

        # resize the image and grab the new image dimensions
        self.image = cv.resize(self.image, (newW, newH))
        (self.imageHeight, self.imageWidth) = self.image.shape[:2]


    def detectTexts(self):
        self.image = gammaCorrection(self.image);

        # define the two output layer names for the EAST detector model that
        # we are interested -- the first is the output probabilities and the
        # second can be used to derive the bounding box coordinates of text
        layerNames = [
                "feature_fusion/Conv_7/Sigmoid",
                "feature_fusion/concat_3"
        ]

        # load the pre-trained EAST text detector
        print("[INFO] loading EAST text detector...")
        net = cv.dnn.readNet(os.path.join(self.mainDir, "frozen_east_text_detection.pb"))

        # construct a blob from the image and then perform a forward pass of
        # the model to obtain the two output layer sets
        blob = cv.dnn.blobFromImage(self.image, 1.0, (self.imageWidth, self.imageHeight),
                (123.68, 116.78, 103.94), swapRB=True, crop=False)
        start = time.time()
        net.setInput(blob)
        (scores, geometry) = net.forward(layerNames)
        end = time.time()

        # show timing information on text prediction
        print("[INFO] text detection took {:.6f} seconds".format(end - start))
        (rects, confidences) = self.decodeResults(scores, geometry);

        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        boxes = self.scaleBoundingBoxes(boxes);

        return (boxes, confidences);


    def decodeResults(self, scores, geometry):
        # grab the number of rows and columns from the scores volume, then
        # initialize our set of bounding box rectangles and corresponding
        # confidence scores
        (numRows, numCols) = scores.shape[2:4]
        rects = []
        confidences = []

        # loop over the number of rows
        for y in range(0, numRows):
            # extract the scores (probabilities), followed by the geometrical
            # data used to derive potential bounding box coordinates that
            # surround text
            scoresData = scores[0, 0, y]
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]

            # loop over the number of columns
            for x in range(0, numCols):
                # if our score does not have sufficient probability, ignore it
                if scoresData[x] < self.minConfidence:
                        continue

                # compute the offset factor as our resulting feature maps will
                # be 4x smaller than the input image
                (offsetX, offsetY) = (x * 4.0, y * 4.0)

                # extract the rotation angle for the prediction and then
                # compute the sin and cosine
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)

                # use the geometry volume to derive the width and height of
                # the bounding box
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]

                # compute both the starting and ending (x, y)-coordinates for
                # the text prediction bounding box
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                startX = int(endX - w)
                startY = int(endY - h)

                # add the bounding box coordinates and probability score to
                # our respective lists
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])

        return (rects, confidences);


    def scaleBoundingBoxes(self, boxes):
        scaledBoxes = []
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios, since the boxes were obtained from the resized image
            startX = int(startX * self.ratioW)
            startY = int(startY * self.ratioH)
            endX = int(endX * self.ratioW)
            endY = int(endY * self.ratioH)

            scaledBoxes.append((startX, startY, endX, endY));

        return scaledBoxes;


    def drawTextRegions(self, boxes):
        resultImage = self.origImage.copy();
        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # draw the bounding box on the image
            cv.rectangle(resultImage, (startX, startY), (endX, endY), (0, 255, 0), 2)

        return resultImage;

