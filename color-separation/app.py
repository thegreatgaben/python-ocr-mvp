import cv2
import numpy
import copy
from modules.utils import getImageFileNames, viewImage, averageIntensityValue, smartInvert
from modules.edge import cannyEdge
from modules.hist import histBackProj, equalizeSaturation, showRGBHistogram
from modules.thresh import otsu, otsu_multi_grey, otsu_multi_rgb, otsu_multi_rgb2, otsu_multi_hsv
from modules.color import simpleColorBalance, invert


class ColorSeparationEngine:
    def __init__(self):
        print('Color separation class initialised.')
        self.images = []
        self.originals = []
        self.cache = []
        self.path = ''

    def loadImages(self, path):
        self.path = path
        filenames = getImageFileNames(path)
        filenames.sort()
        for file in filenames:
            current_file = cv2.imread('{}/{}'.format(path, file))
            self.images.append(current_file)
        self.originals = self.images
        print('{} images loaded from {}'.format(len(filenames), path))

    def reloadImages(self):
        self.loadImages(self.path)

    def setCache(self):
        self.cache = copy.deepcopy(self.images)

    def restoreFromCache(self):
        self.images = copy.deepcopy(self.cache)

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
        print('otsuThresh run on {} images'.format(len(self.images)))

    def otsuThreshMultiGrey(self, classes=3):
        new_images = []
        for image in self.images:
            new_images.append(otsu_multi_grey(image, classes))
        self.images = new_images
        print('otsuThreshMultiGrey run on {} images (classes={})'.format(
            len(self.images), classes))

    def otsuThreshMultiRGB(self, classes=3):
        new_images = []
        for image in self.images:
            bgr = otsu_multi_rgb(image, classes)
            for channel in bgr:
                new_images.append(channel)
        print('otsuThreshMultiRGB run on {} images (classes={}). {} images produced.'.format(
            len(self.images), classes, len(new_images)))
        self.images = new_images

    def otsuThreshMultiRGBv2(self, classes=3):
        new_images = []
        for image in self.images:
            bgr = otsu_multi_rgb2(image, classes)
            for channel in bgr:
                new_images.append(channel)
        print('otsuThreshMultiRGBv2 run on {} images (classes={}). {} images produced.'.format(
            len(self.images), classes, len(new_images)))
        self.images = new_images

    def otsuThreshMultiHSV(self, classes=3, threshold=True):
        new_images = []
        for image in self.images:
            bgr = otsu_multi_hsv(image, classes, threshold)
            for channel in bgr:
                new_images.append(channel)
        print('otsuThreshMultiHSV run on {} images (classes={}). {} images produced.'.format(
            len(self.images), classes, len(new_images)))
        self.images = new_images

    def colorBalance(self, percent=10):
        new_images = []
        for image in self.images:
            new_images.append(simpleColorBalance(image, percent))
        self.images = new_images
        print('colorBalance run on {} images (percent={})'.format(
            len(self.images), percent))

    def smartInvert(self):
        new_images = []
        for image in self.images:
            new_images.append(smartInvert(image))
        self.images = new_images
        print('smartInverted {} images'.format(len(self.images)))


def edgeDetect1():  # blur, canny edge detection
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(6)
    C.edgeDetection(100, 150)
    C.writeOutput('output')


def histBackProj1():  # blur, histogram back projection
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(6)
    C.setCache()
    for i in range(3, 20, 2):
        C.histBackProjection(i)
        C.writeOutput('output')
        input('i={}, press any key'.format(i))
        C.restoreFromCache()


def multiOtsuTest1():  # greyscaled multi level otsu
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.resize(2000, 2000)
    C.blur(4)
    C.otsuThreshMultiGrey(3)
    C.writeOutput('output')


def multiOtsuTest2():  # RGB multi level otsu
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.blur(6)
    C.otsuThreshMultiRGB(3)
    C.writeOutput('output')


def colorBalanceTest1(src):  # color balancing
    img = cv2.imread(src)  # 'images/img1.jpg'
    eq = simpleColorBalance(img, 10)
    showRGBHistogram(img)
    showRGBHistogram(eq)
    viewImage(img)
    viewImage(eq)


def colorBalanceTest2():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.writeOutput('output')


def multiOtsuTest3():
    C = ColorSeparationEngine()
    C.loadImages('images')
    # C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiRGB(2)
    # C.smartInvert()
    C.writeOutput('output')


def multiOtsuTest4():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiRGBv2(2)
    C.smartInvert()
    C.writeOutput('output')


def multiOtsuTest5():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiHSV(2)
    C.writeOutput('output2c-4b')


def multiOtsuTest5p5():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.otsuThreshMultiHSV(2)
    C.writeOutput('output2c-0b')


def multiOtsuTest6():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.otsuThreshMultiHSV(3, False)
    C.writeOutput('output-nt')


def multiOtsuTest7():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(20)
    C.otsuThreshMultiHSV(2)
    C.writeOutput('output2c-20b')


def multiOtsuTest8():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(20)
    C.otsuThreshMultiRGB(2)
    C.smartInvert()
    C.writeOutput('output2c-20b-nc')


def multiOtsuTest9():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiRGB(2)
    C.smartInvert()
    C.writeOutput('output2c-4b-nc')


def multiOtsuTest10():
    C = ColorSeparationEngine()
    C.loadImages('images')
    C.colorBalance()
    C.blur(4)
    C.otsuThreshMultiRGB(3)
    C.smartInvert()
    C.writeOutput('output3c-4b-nc')


if __name__ == "__main__":
    multiOtsuTest5()
    multiOtsuTest5p5()
    multiOtsuTest6()
    multiOtsuTest7()
    multiOtsuTest8()
    multiOtsuTest9()
    multiOtsuTest10()
