from east_text_detection import EASTTextDetection
from mser_text_detection import MSERTextDetection
from ocr import OCREngine
from img_utils import outputImage

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
    ap.add_argument("-mser", action='store_true',
            help="selects the MSER text detection method");
    ap.add_argument("-east", action='store_true',
            help="selects the EAST text detection method");
    args = vars(ap.parse_args())

    origImage = None;
    if (args["mser"]):
        mser = MSERTextDetection(imagePath=args["image"]);
        boxes = mser.detectTexts();
        origImage = mser.origImage;
    elif (args["east"]):
        east = EASTTextDetection(imagePath=args["image"], minConfidence=args["min_confidence"]);
        (boxes, confidences) = east.detectTexts();
        resultImage = east.drawTextRegions(boxes);
        east.showResults(resultImage);
        origImage = east.origImage;

    ocrEngine = OCREngine(language=args["language"], padding=True, roiPadding=0.025);
    ocrEngine.performOCR(origImage, boxes);

