from text_detection import TextDetection
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
    args = vars(ap.parse_args())

    textDetector = TextDetection(imagePath=args["image"], minConfidence=args["min_confidence"]);
    resultImage = textDetector.detectTexts();

    imageName = os.path.basename(args["image"]);
    outputImage(resultImage, imageName);
