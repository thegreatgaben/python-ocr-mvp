import img_utils

import cv2 as cv
import pytesseract

class OCREngine:

    def __init__(self, language, padding=False, roiPadding=0.05, imageFileExt='jpg'):
        self.paddingEnabled = padding;
        self.roiPadding = roiPadding;
        self.tesseractConfig = ("-l {} --oem 2 --psm 7".format(language));
        self.imageFileExt = imageFileExt;


    def performOCR(self, image, boxes, showResult=False):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY);
        (imageHeight, imageWidth) = image.shape[:2]

        index = 0;
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

            # Some preprocessing to (hopefully) improve OCR results
            textImage = gray[startY:endY, startX:endX];
            textImage = cv.resize(textImage, None, fx=2, fy=2);

            gaussian = cv.GaussianBlur(textImage, (5, 5), 0);
            textImage = cv.addWeighted(textImage, 1.5, gaussian, -0.5, 0);

            _, binTextImage = cv.threshold(textImage, 0, 255, cv.THRESH_BINARY_INV+cv.THRESH_OTSU);
            # Opening morphological operation to remove noise
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5));
            binTextImage = cv.morphologyEx(binTextImage, cv.MORPH_OPEN, kernel);

            finalTextImage = binTextImage;

            text = pytesseract.image_to_string(finalTextImage, config=self.tesseractConfig);
            if text != '':
                print(text);
                textHeight = finalTextImage.shape[0];
                cv.putText(textImage, text, (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv.LINE_AA);
                img_utils.outputImage(textImage, 'ocr/word_{}.{}'.format(index, self.imageFileExt));
                img_utils.outputImage(finalTextImage, 'ocr/word_{}_bin.{}'.format(index, self.imageFileExt));

            index += 1;


