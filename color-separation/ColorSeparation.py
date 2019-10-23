import cv2
import numpy as np
from copy import deepcopy
from modules.utils import getImageFileNames, viewImage, averageIntensityValue, smartInvert, deleteAllItems, deleteAllBitmaps
from modules.edge import cannyEdge
from modules.hist import histBackProj, equalizeSaturation, showRGBHistogram
from modules.thresh import otsu, otsu_multiclass_grey, otsu_multiclass_hsv, otsu_multiclass_rgb
from modules.color import simpleColorBalance, invert


class ColorSeparationEngine:
    def __init__(self):
        print('Color separation class initialised.')
        self.images = []
        self.originals = []
        self.cache = []
        self.path = ''

    def getImagePaths(self, path):
        filenames = getImageFileNames(path)
        filenames.sort()
        for i in range(len(filenames)):
            filenames[i] = path + '/' + filenames[i]
        return filenames

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
        self.cache = deepcopy(self.images)

    def restoreFromCache(self):
        self.images = deepcopy(self.cache)

    def clearCache(self):
        self.cache = []

    def clearFolder(self, path):
        deleteAllBitmaps(path)

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
            len(self.images), blur_size
        ))

    def histBackProjection(self, bins=10):
        new_images = []
        for image in self.images:
            new_images.append(histBackProj(image, bins)[0])
        self.images = new_images
        print('Histogram back projection run on {} images ({} bins)'.format(
            len(self.images), bins
        ))

    def edgeDetection(self, t1=20, t2=40):
        new_images = []
        for image in self.images:
            out_img = cannyEdge(image, t1, t2)
            new_images.append(out_img)
        self.images = new_images
        print('edgeDetection run on {} images (t1={}, t2={})'.format(
            len(self.images), t1, t2
        ))

    def otsuThresh(self):
        new_images = []
        for image in self.images:
            new_images.append(otsu(image))
        self.images = new_images
        print('otsuThresh run on {} images'.format(len(self.images)))

    def otsuThreshMultiGrey(self, classes=2):
        new_images = []
        for image in self.images:
            new_images.append(otsu_multiclass_grey(image, classes))
        self.images = new_images
        print('otsuThreshMultiGrey run on {} images (classes={})'.format(
            len(self.images), classes))

    def otsuThreshMultiRGB(self, classes=2):
        new_images = []
        for image in self.images:
            bgr = otsu_multiclass_rgb(image, classes)
            for channel in bgr:
                new_images.append(channel)
        print('otsuThreshMultiRGB run on {} images (classes={}). {} images produced.'.format(
            len(self.images), classes, len(new_images)))
        self.images = new_images

    def otsuThreshMultiHSV(self, classes=2, threshold=True, hues=[(115, 35), (55, 35), (0, 35)], colorize=False):
        new_images = []
        for image in self.images:
            bgr = otsu_multiclass_hsv(image, classes, threshold, hues)
            print(len(bgr))
            if (len(bgr) > 0):
                zeros = np.zeros(np.shape(bgr[0]), dtype=np.uint8)
                for i in range(len(bgr)):
                    if (len(bgr) == 3 and colorize):
                        pre_merge = [zeros] * len(bgr)
                        pre_merge[i] = bgr[i]
                        colorized = cv2.merge(tuple(pre_merge))
                        new_images.append(colorized)
                    else:
                        new_images.append(bgr[i])
        print('otsuThreshMultiHSV run on {} images (classes={}). {} images produced.'.format(
            len(self.images), classes, len(new_images)
        ))
        self.images = new_images

    def colorBalance(self, percent=10):
        new_images = []
        for image in self.images:
            new_images.append(simpleColorBalance(image, percent))
        self.images = new_images
        print('colorBalance run on {} images (percent={})'.format(
            len(self.images), percent
        ))

    def smartInvert(self):
        new_images = []
        for image in self.images:
            new_images.append(smartInvert(image))
        self.images = new_images
        print('smartInverted {} images'.format(len(self.images)))