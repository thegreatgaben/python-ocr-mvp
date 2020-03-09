import img_utils

import os
import cv2 as cv
import pytesseract

class OCREngine:

    def __init__(self, padding=False, roiPadding=0.05, diagnostics=False):
        self.paddingEnabled = padding;
        self.roiPadding = roiPadding;
        self.tessDataPath = os.path.join(os.path.dirname(__file__), "big_assets/tesseract/training_data/");
        self.tesseractConfig = "-l {} --oem 1 --psm 7 --tessdata-dir {}";
        self.diagnostics = diagnostics;


    def performOCR(self, image, boxes, imageMeta, languages="eng", showResult=False):
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY);

        recognisedTexts = [];
        index = 0;

        tessConfig = self.tesseractConfig.format(languages, self.tessDataPath);
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
                endX = min(imageMeta["width"], endX + (dX * 2))
                endY = min(imageMeta["height"], endY + (dY * 2))

            # Some preprocessing to (hopefully) improve OCR results
            textImage = gray[startY:endY, startX:endX];
            textImage = cv.resize(textImage, None, fx=2, fy=2);

            gaussian = cv.GaussianBlur(textImage, (5, 5), 0);
            textImage = cv.addWeighted(textImage, 1.5, gaussian, -0.5, 0);

            _, binTextImage = cv.threshold(textImage, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU);
            # Opening morphological operation to remove noise
            kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5));
            binTextImage = cv.morphologyEx(binTextImage, cv.MORPH_OPEN, kernel);

            finalTextImage = binTextImage;

            text = pytesseract.image_to_string(finalTextImage, config=tessConfig);
            if text != '':
                print(text);
                recognisedTexts.append({
                    "text": text,
                    "left": int(startX),
                    "ratioLeft": startX/imageMeta["width"],
                    "top": int(startY),
                    "ratioTop": startY/imageMeta["height"],
                    # Hard coded values for now
                    "fontFamily": "Arial",
                    "fontSize": 20
                });
                if self.diagnostics:
                    textHeight = finalTextImage.shape[0];
                    cv.putText(textImage, text, (0, 50), cv.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 2, cv.LINE_AA);
                    img_utils.outputImage(textImage, 'ocr/word_{}.{}'.format(index, imageMeta["ext"]));
                    img_utils.outputImage(finalTextImage, 'ocr/word_{}_bin.{}'.format(index, imageMeta["ext"]));

            index += 1;

        return recognisedTexts;


