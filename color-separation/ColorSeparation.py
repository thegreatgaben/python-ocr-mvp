import cv2
import numpy as np
from copy import deepcopy
from modules.utils import getImageFileNames, viewImage, averageIntensityValue, smartInvert, deleteAllItems, deleteAllBitmaps, getSubdirectories
from modules.edge import cannyEdge
from modules.hist import histBackProj, equalizeSaturation, showRGBHistogram
from modules.thresh import otsu, otsu_multiclass_grey, otsu_multiclass_hsv, otsu_multiclass_rgb
from modules.color import simpleColorBalance, invert


class ColorSeparationEngine:
    def __init__(self):
        print('[CS] Color separation class initialised.')
        self.images = []
        self.metadata_images = []
        self.originals = []
        self.cache = []
        self.metadata_cache = []
        self.path = ''
        self.writeFormat = 'bmp'

    def reinitialize(self):
        print('[CS] Color separation class reinitialised.')
        self.images = []
        self.metadata_images = []
        self.originals = []
        self.cache = []
        self.metadata_cache = []
        self.path = ''
        self.writeFormat = 'bmp'

    def loadImages(self, imageArray, reinitialize=True):
        if reinitialize:
            self.reinitialize()
        for i in range(len(imageArray)):
            self.loadImage(imageArray[i], index=i, reinitialize=False, log=False)
        print('[CS] {} images loaded.'.format(len(imageArray)))


    def loadImage(self, image, index=0, reinitialize=True, log=True):
        if reinitialize:
            self.reinitialize()
        metadata = {}
        (imgHeight, imgWidth) = image.shape[:2]
        metadata['width'] = imgWidth
        metadata['height'] = imgHeight
        metadata['index'] = index
        metadata['color_type'] = 'RGB'
        self.images.append(image)
        self.metadata_images.append(deepcopy(metadata))
        self.originals = self.images
        if log:
            print('[CS] 1 Image loaded ({} * {}).'.format(imgWidth, imgHeight))

    # def loadImagesFromPath(self, path, reinitialize=True):
    #     if reinitialize:
    #         self.reinitialize()
    #     self.path = path
    #     filenames = getImageFileNames(path)
    #     filenames.sort()
    #     for file in filenames:
    #         current_file = cv2.imread('{}/{}'.format(path, file))
    #         self.images.append(current_file)
    #         (imageHeight, imageWidth) = current_file.shape[:2]
    #         print('height:' + imageHeight)
    #         print('width:' + imageHeight)
    #         print('path:' + '{}/{}'.format(path, file))
    #     self.originals = self.images  # keep originals
    #     print('[CS] {} images loaded from {}'.format(len(filenames), path))

    # def loadImageFromPath(self, path):
    #     self.path = path
    #     self.images = [cv2.imread(path)]
    #     self.originals = self.images
    #     print('[CS] {} loaded.'.format(path))

    def getImagePaths(self, path):
        filenames = getImageFileNames(path)
        filenames.sort()
        for i in range(len(filenames)):
            filenames[i] = path + '/' + filenames[i]
        return filenames

    def getSubdirectories(self, path):
        return getSubdirectories(path)

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
            cv2.imwrite("{}/{}.{}".format(out_path, self.metadata_images[i]['index'], self.writeFormat), self.images[i])
        print('[CS] {} images written to ./{}'.format(len(self.images), out_path))

    def writeOutputCollate(self, out_path):
        pass
        existingFilenames = getImageFileNames(out_path)
        for i in range(len(existingFileNames), len(existingFileNames) + len(self.images)):
            cv2.imwrite("{}/{}.{}".format(out_path, i, self.writeFormat), self.images[i])
        print('[CS] {} images written to ./{}'.format(len(self.images), out_path))

    def resize(self, w=640, h=640):
        new_images = []
        new_metadata = []
        for i in range(len(self.images)):
            resized = cv2.resize(self.images[i], (w, h))
            new_images.append(resized)

            # metadata handling
            (imgHeight, imgWidth) = resized.shape[:2]
            metadata = self.metadata_images[i]
            metadata['width'] = imgWidth
            metadata['height'] = imgHeight
            new_metadata.append(deepcopy(metadata))
        self.images = new_images
        self.metadata_images = new_metadata
        print('[CS] {} images resized ({} * {})'.format(len(self.images), w, h))

    def blur(self, blur_size):
        new_images = []
        for image in self.images:
            new_images.append(cv2.blur(image, (blur_size, blur_size)))
        self.images = new_images
        print('[CS] {} images blurred (blur_size={})'.format(
            len(self.images), blur_size
        ))

    def histBackProjection(self, bins=10):
        new_images = []
        for image in self.images:
            new_images.append(histBackProj(image, bins)[0])
        self.images = new_images
        print('[CS] {} images processed with histogram back projection ({} bins)'.format(
            len(self.images), bins
        ))

    def edgeDetection(self, t1=20, t2=40):
        new_images = []
        new_metadata = []
        for i in range(len(self.images)):
            out_img = cannyEdge(self.images[i], t1, t2)
            new_images.append(out_img)

            # metadata handling
            metadata = self.metadata_images[i]
            metadata['color_type'] = 'Greyscale'
            new_metadata.append(deepcopy(metadata))
        self.images = new_images
        self.metadata_images = new_metadata
        print('[CS] {} images processed with edgeDetection (t1={}, t2={})'.format(
            len(self.images), t1, t2
        ))

    def otsuThresh(self):
        new_images = []
        new_metadata = []
        for i in range(len(self.images)):
            new_images.append(otsu(self.images[i]))

            # metadata handling
            metadata = self.metadata_images[i]
            metadata['color_type'] = 'Greyscale'
            new_metadata.append(deepcopy(metadata))
        self.images = new_images
        self.metadata_images = new_metadata
        print('[CS] {} images processed with otsuThresh'.format(len(self.images)))

    def otsuThreshMultiGrey(self, classes=2):
        new_images = []
        new_metadata = []
        for i in range(len(self.images)):
            new_images.append(otsu_multiclass_grey(self.images[i], classes))
            
            # metadata handling
            metadata = self.metadata_images[i]
            metadata['color_type'] = 'Greyscale'
            new_metadata.append(deepcopy(metadata))
        self.images = new_images
        self.metadata_images = new_metadata
        print('[CS] {} images processed with otsuThreshMultiGrey (classes={})'.format(
            len(self.images), classes))

    def otsuThreshMultiRGB(self, classes=2):
        new_images = []
        new_metadata = []
        channels = ['RGB_B', 'RGB_G', 'RGB_R']
        for i in range(len(self.images)):
            bgr = otsu_multiclass_rgb(self.images[i], classes)
            for j in range(len(bgr)):
                new_images.append(bgr[j])

                # metadata handling
                metadata = self.metadata_images[i]
                metadata['index'] = len(new_metadata)
                metadata['color_type'] = 'RGB'
                metadata['color_channel'] = channels[i]
                new_metadata.append(deepcopy(metadata))
        print('[CS] {} images processed with otsuThreshMultiRGB (classes={}). {} images produced.'.format(
            len(self.images), classes, len(new_images)))
        self.images = new_images
        self.metadata_images = new_metadata

    def otsuThreshMultiHSV(self, classes=2, threshold=True, hues=[(115, 35), (55, 35), (0, 35)], colorize=False):
        new_images = []
        new_metadata = []
        for i in range(len(self.images)):
            channels, channel_metadata = otsu_multiclass_hsv(self.images[i], classes, threshold, hues)
            if (len(channels) > 0):
                zeros = np.zeros(np.shape(channels[0]), dtype=np.uint8)
                for j in range(len(channels)):
                    # metadata handling
                    metadata = self.metadata_images[i]
                    metadata['index'] = len(new_metadata)
                    metadata['hue'] = channel_metadata[j]['hue']
                    metadata['hue_variance'] = channel_metadata[j]['hue_variance']
                    # TODO: colorize not only to rgb, but to the actual hue value
                    if (len(channels) == 3 and colorize):
                        pre_merge = [zeros] * len(channels)
                        pre_merge[j] = channels[j]
                        colorized = cv2.merge(tuple(pre_merge))
                        new_images.append(colorized)
                        # metadata handling
                        metadata['color_type'] = 'RGB'
                        new_metadata.append(deepcopy(metadata))
                    else:
                        new_images.append(bgr[i])
                        # metadata handling
                        metadata['color_type'] = 'Greyscale'
                        new_metadata.append(deepcopy(metadata))
        print('[CS] {} images processed with otsuThreshMultiHSV (classes={}). {} images produced.'.format(
            len(self.images), classes, len(new_images)
        ))
        self.images = new_images
        self.metadata_images = new_metadata

    def colorBalance(self, percent=10):
        new_images = []
        for image in self.images:
            new_images.append(simpleColorBalance(image, percent))
        self.images = new_images
        print('[CS] {} images processed with colorBalance (percent={})'.format(
            len(self.images), percent
        ))

    def smartInvert(self):
        new_images = []
        for image in self.images:
            new_images.append(smartInvert(image))
        self.images = new_images
        print('[CS] {} images processed with smartInvert'.format(len(self.images)))

