from text_detection import TextDetection
from ocr import OCREngine
from img_utils import outputImage, testMSER

import argparse
import os
import cv2 as cv

if __name__ == "__main__":
    print(cv.__version__);
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", type=str,
            help="path to input image")
    ap.add_argument("-c", "--min-confidence", type=float, default=0.75,
            help="minimum probability required to inspect a region")
    ap.add_argument("-l", "--language", type=str,
            help="selected language to recognise refer to tesseract's manual page for format")
    args = vars(ap.parse_args())

    imagePath = args["image"];
    image = cv.imread(imagePath);
    boxes = testMSER(image);
    '''
    textDetector = TextDetection(imagePath=args["image"], minConfidence=args["min_confidence"]);
    (boxes, confidences) = textDetector.detectTexts();
    resultImage = textDetector.drawTextRegions(boxes);

    imageName = os.path.basename(args["image"]);
    outputImage(resultImage, imageName);
    '''

    ocrEngine = OCREngine(language=args["language"], padding=True);
    ocrEngine.performOCR(image, boxes);

