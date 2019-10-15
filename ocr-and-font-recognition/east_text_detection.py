'''
Based on this tutorial here:
https://www.pyimagesearch.com/2018/08/20/opencv-text-detection-east-text-detector/
'''

from text_detection import TextDetection
import img_utils

from imutils.object_detection import non_max_suppression
import math
import numpy as np
import time
import os
import cv2 as cv

class EASTTextDetection(TextDetection):

    def __init__(self, minConfidence, diagnostics=False):
        TextDetection.__init__(self);
        self.minConfidence = minConfidence;
        self.diagnostics = diagnostics;


    def detectTexts(self, image, imageMeta):
        # set the new width and height and then determine the ratio in change
        # for both the width and height
        # NOTE: The EAST text detector only accepts image with dimensions of multiples of 32
        (newW, newH) = (math.ceil(imageMeta["width"]/32) * 32, math.ceil(imageMeta["height"]/32) * 32)
        imageMeta["ratioW"] = imageMeta["width"] / float(newW)
        imageMeta["ratioH"] = imageMeta["height"] / float(newH)

        preprocessed = cv.resize(image, (newW, newH))
        preprocessed = img_utils.gammaCorrection(preprocessed);

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
        blob = cv.dnn.blobFromImage(preprocessed, 1.0, (newW, newH),
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
        boxes = self.scaleBoundingBoxes(boxes, imageMeta);

        if self.diagnostics:
            vis = self.drawTextRegions(image, boxes);
            filename = 'east_detected_texts.{}'.format(imageMeta["ext"]);
            img_utils.outputImage(vis, filename);

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


    def scaleBoundingBoxes(self, boxes, imageMeta):
        scaledBoxes = []
        for (startX, startY, endX, endY) in boxes:
            # scale the bounding box coordinates based on the respective
            # ratios, since the boxes were obtained from the resized image
            startX = int(startX * imageMeta["ratioW"])
            startY = int(startY * imageMeta["ratioH"])
            endX = int(endX * imageMeta["ratioW"])
            endY = int(endY * imageMeta["ratioH"])

            scaledBoxes.append((startX, startY, endX, endY));

        return scaledBoxes;


