import os
import numpy as np
import cv2 as cv


def basicLinearTransform(image):
    '''
    Increase the contrast and brightness of the image in a linear manner
    '''
    alpha = 1.0 # Simple contrast control
    beta = 0    # Simple brightness control

    # Initialize values
    print(' Basic Linear Transforms ')
    print('-------------------------')
    try:
        alpha = float(input('* Enter the alpha value [1.0-3.0]: '))
        beta = int(input('* Enter the beta value [0-100]: '))
    except ValueError:
        print('Error, not a number')

    new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
    return new_image;


def gammaCorrection(image, gamma=0.25):
    ## [changing-contrast-brightness-gamma-correction]
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    res = cv.LUT(image, lookUpTable)
    return res


def outputImage(image, imageName):
    # OpenCV does not create the directory for you
    outputPath = os.path.join(os.path.dirname(__file__), 'test/output');
    if not os.path.exists(outputPath):
        os.mkdir(outputPath);
    # show the output image
    cv.imwrite(os.path.join(outputPath, imageName), image);


def testMSER(image, showResult=False):
    mser = cv.MSER_create()

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    blurred = cv.GaussianBlur(gray, (5, 5), 0);

    vis = image.copy()

    _, boxes = mser.detectRegions(blurred)
    mappedBoxes = []
    for (x, y, w, h) in boxes:
        mappedBoxes.append([x, y, x + w, y + h]);

    mappedBoxes = non_max_suppression_fast(np.array(mappedBoxes), overlapThresh=0.3);
    for (startX, startY, endX, endY) in mappedBoxes:
        cv.rectangle(vis, (startX, startY), (endX, endY), (0, 255, 0), 1);

    if showResult:
        while True:
            cv.imshow('image', vis)
            if cv.waitKey(5) == 27:
                break

    return mappedBoxes;



def detectAndRemoveRects(image, preprocessed, showResult=False):
    contourList, _ = cv.findContours(preprocessed.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    resultImage = image.copy();
    detectedRects = []
    for contour in contourList:
        perimeter = cv.arcLength(contour, True);
        approx = cv.approxPolyDP(contour, 0.04 * perimeter, True);
        if len(approx) == 4:
            (x, y, w, h) = cv.boundingRect(approx)
            rect = [x, y, x+w, y+h];
            detectedRects.append(rect);
            cv.rectangle(resultImage, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 1);

    if showResult:
        while True:
            cv.imshow('image', resultImage);
            cv.imshow('preprocessed', preprocessed);
            if cv.waitKey(5) == 27:
                break


def non_max_suppression_fast(boxes, overlapThresh):
    # if there are no boxes, return an empty list
    if len(boxes) == 0:
        return []

    # if the bounding boxes integers, convert them to floats --
    # this is important since we'll be doing a bunch of divisions
    if boxes.dtype.kind == "i":
        boxes = boxes.astype("float")

    # initialize the list of picked indexes
    pick = []

    # grab the coordinates of the bounding boxes
    x1 = boxes[:,0]
    y1 = boxes[:,1]
    x2 = boxes[:,2]
    y2 = boxes[:,3]

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    area = (x2 - x1 + 1) * (y2 - y1 + 1)
    idxs = np.argsort(y2)

    # keep looping while some indexes still remain in the indexes
    # list
    while len(idxs) > 0:
        # grab the last index in the indexes list and add the
        # index value to the list of picked indexes
        last = len(idxs) - 1
        i = idxs[last]
        pick.append(i)

        # find the largest (x, y) coordinates for the start of
        # the bounding box and the smallest (x, y) coordinates
        # for the end of the bounding box
        xx1 = np.maximum(x1[i], x1[idxs[:last]])
        yy1 = np.maximum(y1[i], y1[idxs[:last]])
        xx2 = np.minimum(x2[i], x2[idxs[:last]])
        yy2 = np.minimum(y2[i], y2[idxs[:last]])

        # compute the width and height of the bounding box
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)

        # compute the ratio of overlap
        overlap = (w * h) / area[idxs[:last]]

        # delete all indexes from the index list that have
        idxs = np.delete(idxs, np.concatenate(([last],
                np.where(overlap > overlapThresh)[0])))

    # return only the bounding boxes that were picked using the
    # integer data type
    return boxes[pick].astype("int")

