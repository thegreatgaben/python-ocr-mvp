from img_utils import *

import cv2 as cv
import pytesseract

class OCREngine:

    def __init__(self, language, padding=False, roiPadding=0.1):
        self.paddingEnabled = padding;
        self.roiPadding = roiPadding;
        self.tesseractConfig = ("-l {} --oem 1 --psm 7".format(language));


    def performOCR(self, image, boxes):
        (imageHeight, imageWidth) = image.shape[:2]
        for (startX, startY, endX, endY) in boxes:
            if self.paddingEnabled:
                # in order to obtain a better OCR of the text we can potentially
                # apply a bit of padding surrounding the bounding box -- here we
                # are computing the deltas in both the x and y directions
                dX = int((endX - startX) * self.roiPadding)
                dY = int((endY - startY) * self.roiPadding)

                # apply padding to each side of the bounding box, respectively
                startX = max(0, startX - dX)
                startY = max(0, startY - dY)
                endX = min(imageWidth, endX + (dX * 2))
                endY = min(imageHeight, endY + (dY * 2))

            textImage = image[startY:endY, startX:endX];
            binTextImage = binarizeImage(textImage);

            text = pytesseract.image_to_string(binTextImage, config=self.tesseractConfig);
            print(text);

            cv.imshow('test', binTextImage);
            cv.waitKey(0);

