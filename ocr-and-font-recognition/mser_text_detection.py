from text_detection import TextDetection
from swt import SWTScrubber
import img_utils
import skimage.measure
from matplotlib import pyplot as plt

import os
import numpy as np
import cv2 as cv

class MSERTextDetection(TextDetection):

    def __init__(self, diagnostics=False):
        TextDetection.__init__(self);
        self.diagnostics = diagnostics;


    def getOutputFilePath(self, filename):
        return os.path.join(self.outputPath, filename);


    def detectTexts(self, image, imageMeta, outputFileName):
        mser = cv.MSER_create()

        # Preprocessing
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
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

        mappedBoxes = self.filterTextByGeometricProperties(blurred, mappedBoxes, imageMeta);
        # mappedBoxes = self.filterTextBySWT(blurred, mappedBoxes, imageMeta);

        vis = self.drawTextRegions(image, mappedBoxes);
        img_utils.outputImage(vis, outputFileName);

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


    def filterTextByGeometricProperties(self, preprocessed, boxes, imageMeta):
        filteredBoxes = [];
        _, binImage = cv.threshold(preprocessed, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU);
        if self.diagnostics:
            img_utils.outputImage(binImage, "bin.{}".format(imageMeta["ext"]));

        for (x1, y1, x2, y2) in boxes:
            w = abs(x1 - x2) + 1;
            h = abs(y1 - y2) + 1;

            if w/imageMeta["width"] < 0.01 or h/imageMeta["height"] < 0.01:
                continue;

            aspectRatio = w/h;
            if aspectRatio < 0.4 or aspectRatio > 20.0:
                continue;

            region = binImage[y1:y2, x1:x2];
            labelRegion = skimage.measure.label(region);
            props = skimage.measure.regionprops(labelRegion);

            if len(props) == 0:
                continue;

            # Measures the ciruclar nature of a given region
            eccentricity = np.median(np.array(list(map(lambda x: x.eccentricity, props))));
            # Ratio of pixels in the region to pixels in the total bounding box. Computed as area / (rows * cols)
            extent = np.median(np.array(list(map(lambda x: x.extent, props))));
            # Ratio of pixels in the region to pixels of the convex hull image
            solidity = np.median(np.array(list(map(lambda x: x.solidity, props))));
            # Euler characteristic of region. Computed as number of objects (= 1) subtracted by number of holes (8-connectivity).
            euler = np.array(list(map(lambda x: x.euler_number, props)));

            if self.diagnostics:
                print("Eccentricity: {}".format(eccentricity));
                print("Extent: {}".format(extent));
                print("Solidity: {}".format(solidity));
                print("Euler Number: {}".format(euler));

                cv.imshow('image', region);
                cv.waitKey(0);

            if extent == 1.0 or solidity == 1.0:
                continue;

            if len(props) == 1 and (extent > 0.8 or solidity > 0.8):
                continue;

            # Languages like Chinese would definitely have characters which have more holes in connectivity
            if min(euler) < -10:
                continue;

            filteredBoxes.append([x1, y1, x2, y2]);

        cv.destroyAllWindows();

        return filteredBoxes;


    def filterTextBySWT(self, preprocessed, boxes, imageMeta):
        filteredBoxes = [];
        swt = SWTScrubber();
        (edges, sobelx, sobely, theta) = swt.create_derivative(preprocessed);

        darkOnBright = img_utils.detectDarkOnBrightImage(preprocessed);

        i = 0;
        for (x1, y1, x2, y2) in boxes:
            (textSWT, componentsMap) = swt.scrubWithDerivative(
                    edges[y1:y2, x1:x2],
                    sobelx[y1:y2, x1:x2],
                    sobely[y1:y2, x1:x2],
                    theta[y1:y2, x1:x2],
                    darkOnBright
            );
            variances = [];
            for label,component in componentsMap.items():
                swtVariance = np.var(textSWT[np.nonzero(component)]);
                if swtVariance > 0:
                    variances.append(swtVariance);

            if self.diagnostics:
                img_utils.outputImage(edges[y1:y2, x1:x2], "swt/candidates/candidate_{}_edges.{}".format(i, imageMeta["ext"]));
                img_utils.outputImage(textSWT * 100, "swt/candidates/candidate_{}_swt.{}".format(i, imageMeta["ext"]));

            i += 1;
            if len(variances) == 0:
                continue;

            medianVariance = np.median(np.array(variances));
            if medianVariance < 0.2 or medianVariance > 10.0:
                continue;

            filteredBoxes.append([x1, y1, x2, y2]);

        return filteredBoxes;

