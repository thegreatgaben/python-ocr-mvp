import cv2
import numpy
from modules.utils import getImageFileNames
from modules.edge import cannyEdge
from modules.hist import histBackProj
from modules.thresh import otsu, otsu_multi_grey, otsu_multi_rgb


class ColorSepTests:
    def __init__(self):
        print('Color separation class initialised.')
        self.images = []
        self.originals = []
        self.cache = []

    def loadImages(self, path):
        filenames = getImageFileNames(path)
        filenames.sort()
        for file in filenames:
            current_file = cv2.imread('{}/{}'.format(path, file))
            self.images.append(current_file)
        self.originals = self.images
        print('{} images loaded'.format(len(filenames)))

    def setCache(self):
        self.cache = self.images

    def restoreFromCache(self):
        self.images = self.cache

    def clearCache(self):
        self.cache = []

    def writeOutput(self, out_path):
        for i in range(len(self.images)):
            cv2.imwrite("{}/{}.bmp".format(out_path, i), self.images[i])
        print('{} images written to ./{}'.format(len(self.images), out_path))

    def resize(self, w=400, h=400):
        new_images = []
        for image in self.images:
            resized = cv2.resize(image, (w, h))
            new_images.append(resized)
        self.images = new_images
        print('{} images resized ({} * {})'.format(len(self.images), w, h))

    def blur(self, blur_size):
        new_images = []
        for image in self.images:
            new_images.append(cv2.blur(image, (blur_size, blur_size)))
        self.images = new_images
        print('{} images blurred (blur_size={})'.format(
            len(self.images), blur_size))

    def histBackProjection(self, bins=10):
        new_images = []
        for image in self.images:
            new_images.append(histBackProj(image, bins)[0])
        self.images = new_images
        print('Histogram back projection run on {} images ({} bins)'.format(
            len(self.images), bins))

    def edgeDetection(self, t1=20, t2=40):
        new_images = []
        for image in self.images:
            out_img = cannyEdge(image, t1, t2)
            new_images.append(out_img)
        self.images = new_images
        print('edgeDetection run on {} images (t1={}, t2={})'.format(
            len(self.images), t1, t2))

    def otsuThresh(self):
        new_images = []
        for image in self.images:
            new_images.append(otsu(image))
        self.images = new_images

    def otsuThreshMultiGrey(self, classes=3):
        new_images = []
        for image in self.images:
            new_images.append(otsu_multi_grey(image, classes))
        self.images = new_images

    def otsuThreshMultiRGB(self, classes=3):
        new_images = []
        for image in self.images:
            bgr = otsu_multi_rgb(image, classes)
            for channel in bgr:
                new_images.append(channel)
        self.images = new_images


def edgeDetect1():
    C = ColorSepTests()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(6)
    C.edgeDetection(100, 150)
    C.writeOutput('output')


def histBackProj1():
    C = ColorSepTests()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(6)
    C.setCache()
    for i in range(3, 20, 2):
        C.histBackProjection(i)
        C.writeOutput('output')
        input('i={}, press any key'.format(i))
        C.restoreFromCache()


def multiOtsuTest1():
    C = ColorSepTests()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(4)
    C.otsuThreshMultiGrey(3)
    C.writeOutput('output')


def multiOtsuTest2():
    C = ColorSepTests()
    C.loadImages('images')
    C.blur(6)
    C.otsuThreshMultiRGB(3)
    C.writeOutput('output')


if __name__ == "__main__":
    multiOtsuTest2()
