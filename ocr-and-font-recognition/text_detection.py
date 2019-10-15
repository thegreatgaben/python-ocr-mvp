import os
import cv2 as cv

class TextDetection:

    def __init__(self):
        self.mainDir = os.path.dirname(__file__)


    def detectTexts(self):
        pass;


    def drawTextRegions(self, image, boxes):
        resultImage = image.copy();
        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # draw the bounding box on the image
            cv.rectangle(resultImage, (startX, startY), (endX, endY), (0, 255, 0), 4)

        return resultImage;


    def showResults(self, image, resizeDims=None):
        if resizeDims is not None:
            image = cv.resize(image, resizeDims);

        while True:
            cv.imshow('image', image);
            # Break out of loop if ESC key is pressed
            if cv.waitKey(5) == 27:
                break;
        cv.destroyAllWindows();


