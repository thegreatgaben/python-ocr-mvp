import os
import cv2 as cv

class TextDetection:

    def __init__(self, imagePath):
        self.mainDir = os.path.dirname(__file__)

        # load the input image and grab the image dimensions
        self.imageName = os.path.basename(imagePath);
        self.image = cv.imread(imagePath)
        self.origImage = self.image.copy()
        (self.imageHeight, self.imageWidth) = self.image.shape[:2]


    def detectTexts(self):
        pass;


    def drawTextRegions(self, boxes):
        resultImage = self.origImage.copy();
        # loop over the bounding boxes
        for (startX, startY, endX, endY) in boxes:
            # draw the bounding box on the image
            cv.rectangle(resultImage, (startX, startY), (endX, endY), (0, 255, 0), 2)

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


