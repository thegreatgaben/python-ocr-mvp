from img_utils import *

import cv2 as cv
import pytesseract

class OCREngine:

    def __init__(self, language, padding=False, roiPadding=0.05):
        self.paddingEnabled = padding;
        self.roiPadding = roiPadding;
        self.tesseractConfig = ("-l {} --oem 2 --psm 6".format(language));


    def performOCR(self, image, boxes):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY);
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

            textImage = gray[startY:endY, startX:endX];
            textImage = cv.resize(textImage, None, fx=2, fy=2);

            gaussian = cv.GaussianBlur(textImage, (5, 5), 0);
            unsharped = cv.addWeighted(textImage, 1.5, gaussian, -0.5, 0);

            '''
            kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
            kernel = np.array([[0,-1,0], [-1,5,-1], [0,-1,0]])
            sharpened = cv.filter2D(textImage, -1, kernel)
            '''

            _, binTextImage = cv.threshold(unsharped, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU);
            # detectAndRemoveRects(textImage, binTextImage);

            text = pytesseract.image_to_string(binTextImage, config=self.tesseractConfig);
            if text != '':
                print(text);
                while True:
                    cv.imshow('unsharped', unsharped);
                    cv.imshow('bin', binTextImage);
                    if cv.waitKey(5) == 27:
                        break;
                '''
                cv.imshow('bin', binTextImage);
                cv.waitKey(0);
                '''

