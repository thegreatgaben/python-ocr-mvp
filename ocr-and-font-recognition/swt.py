'''
Stroke Width Transform (SWT) implementation

based on the paper:
http://www.math.tau.ac.il/~turkel/imagepapers/text_detection.pdf

OpenCV and Python implementation taken from:
https://github.com/mypetyak/StrokeWidthTransform
'''

from collections import defaultdict
from disjoint_set import DisjointSet
import hashlib
import math
import os
import time

import numpy as np
import cv2 as cv
import scipy.sparse, scipy.spatial

import img_utils

class SWTScrubber:
    def __init__(self, diagnostics=False):
        self.diagnostics = diagnostics;


    def scrub(self, image):
        canny, sobelx, sobely, theta = self.create_derivative(image)
        swt = self._swt(theta, canny, sobelx, sobely)
        shapes = self._connect_components(swt)
        return (swt, shapes);
        '''
        swts, heights, widths, topleft_pts, images = self._find_letters(swt, shapes)
        word_images = self._find_words(swts, heights, widths, topleft_pts, images)

        final_mask = np.zeros(swt.shape)
        for index, word in enumerate(word_images):
            final_mask += word
        return final_mask
        '''


    def scrubWithDerivative(self, edges, sobelx, sobely, theta, darkOnBright=True):
        swtStart = time.clock();
        swt = self._swt(theta, edges, sobelx, sobely, darkOnBright)
        swtEnd = time.clock() - swtStart;

        ccStart = time.clock();
        shapes = self._connect_components(swt)
        ccEnd = time.clock() - ccStart;

        if self.diagnostics:
            print("[INFO] SWT Transform time: {:.2f} seconds".format(swtEnd));
            print("[INFO] Connected Components time: {:.2f} seconds".format(ccEnd));
            print();

        return (swt, shapes);


    def create_derivative(self, image):
        edges = cv.Canny(image, 130, 180)

        # Create gradient map using Sobel
        sobelx64f = cv.Sobel(image, cv.CV_64F,1,0,ksize=-1)
        sobely64f = cv.Sobel(image, cv.CV_64F,0,1,ksize=-1)

        theta = np.arctan2(sobely64f, sobelx64f)
        if self.diagnostics:
            img_utils.outputImage(edges, 'swt/edges.jpg')
            img_utils.outputImage(np.absolute(sobelx64f), 'swt/sobelx64f.jpg')
            img_utils.outputImage(np.absolute(sobely64f), 'swt/sobely64f.jpg')
            # amplify theta for visual inspection
            theta_visible = (theta + np.pi)*255/(2*np.pi)
            img_utils.outputImage(theta_visible, 'swt/theta.jpg')
        return (edges, sobelx64f, sobely64f, theta)


    def _swt(self, theta, edges, sobelx64f, sobely64f, darkOnBright):
        # create empty image, initialized to infinity
        swt = np.empty(theta.shape)
        swt[:] = np.Infinity
        rayList = []

        # The direction in which we travel the gradient depends on the type of text
        # we want to find. For dark text on light background, follow the opposite
        # direction (into the dark area); for light text on dark background, follow
        # the gradient as is.
        gradientDirection = -1 if darkOnBright else 1;
        step_x_g = gradientDirection * sobelx64f
        step_y_g = gradientDirection * sobely64f

        mag_g = np.sqrt( step_x_g * step_x_g + step_y_g * step_y_g )
        grad_x_g = step_x_g / mag_g
        grad_y_g = step_y_g / mag_g

        # now iterate over pixels in image, checking Canny to see if we're on an edge.
        # if we are, follow a normal a ray to either the next edge or image border
        (imageHeight, imageWidth) = edges.shape[:2];
        (yIndices, xIndices) = np.nonzero(edges);
        for (y, x) in list(zip(yIndices, xIndices)):
            grad_x = grad_x_g[y, x]
            grad_y = grad_y_g[y, x]
            ray = [(x, y)]
            prev_x, prev_y, i = x, y, 0
            while True:
                i += 1
                cur_x = math.floor(x + grad_x * i)
                cur_y = math.floor(y + grad_y * i)

                if cur_x != prev_x or cur_y != prev_y:
                    # Reached past image boundaries
                    if cur_x < 0 or cur_x >= imageWidth or cur_y < 0 or cur_y >= imageHeight:
                        break;

                    # found edge,
                    if edges[cur_y, cur_x] > 0:
                        ray.append((cur_x, cur_y))
                        theta_point = theta[y, x]
                        alpha = theta[cur_y, cur_x]

                        ratio = grad_x * -grad_x_g[cur_y, cur_x] + grad_y * -grad_y_g[cur_y, cur_x];
                        if ratio > 1.0:
                            ratio = 1.0;
                        elif ratio < -1.0:
                            ratio = -1.0;

                        # Check that the gradient direction of the newly found edge pixel (q) is roughly opposite
                        # to the current edge pixel (p)
                        if math.acos(ratio) < np.pi/2.0:
                            thickness = math.sqrt( (cur_x - x) * (cur_x - x) + (cur_y - y) * (cur_y - y) )
                            for (rp_x, rp_y) in ray:
                                swt[rp_y, rp_x] = min(thickness, swt[rp_y, rp_x])
                            rayList.append(ray)
                        break
                    ray.append((cur_x, cur_y))
                    prev_x = cur_x
                    prev_y = cur_y

        # Compute median SWT
        for ray in rayList:
            median = np.median([swt[y, x] for (x, y) in ray])
            for (x, y) in ray:
                swt[y, x] = min(median, swt[y, x])

        if self.diagnostics:
            img_utils.outputImage(swt * 100, 'swt/swt.jpg')

        return swt


    def _connect_components(self, swt):
        # STEP: Compute distinct connected components

        # apply Connected Component algorithm, comparing SWT values.
        # components with a SWT ratio less extreme than 1:3 are assumed to be
        # connected. Apply twice, once for each ray direction/orientation, to
        # allow for dark-on-light and light-on-dark texts
        trees = {}
        # Assumption: we'll never have more than 65535-1 unique components
        label_map = np.zeros(shape=swt.shape, dtype=np.uint16)

        # Components are labeled with numbers
        next_label = 1
        # First Pass, raster scan-style
        swt_ratio_threshold = 3.0
        disjointSet = DisjointSet();
        for y in range(swt.shape[0]):
            for x in range(swt.shape[1]):
                sw_point = swt[y, x]
                if sw_point < np.Infinity and sw_point > 0:
                    neighbors = [(y, x-1),   # west
                                 (y-1, x-1), # northwest
                                 (y-1, x),   # north
                                 (y-1, x+1)] # northeast
                    connected_neighbors = None
                    neighborvals = []

                    for neighbor in neighbors:
                        try:
                            sw_n = swt[neighbor]
                            label_n = label_map[neighbor]
                        except IndexError:
                            continue

                        if label_n > 0 and sw_n / sw_point < swt_ratio_threshold and sw_point / sw_n < swt_ratio_threshold:
                            neighborvals.append(label_n)
                            if connected_neighbors:
                                connected_neighbors = disjointSet.Union(connected_neighbors, disjointSet.MakeSet(label_n))
                            else:
                                connected_neighbors = disjointSet.MakeSet(label_n)

                    if not connected_neighbors:
                        # We don't see any connections to North/West
                        trees[next_label] = (disjointSet.MakeSet(next_label))
                        label_map[y, x] = next_label
                        next_label += 1
                    else:
                        # We have at least one connection to North/West
                        label_map[y, x] = min(neighborvals)
                        # For each neighbor, make note that their respective connected_neighbors are connected
                        # for label in connected_neighbors. @todo: do I need to loop at all neighbor trees?
                        trees[connected_neighbors.value] = disjointSet.Union(trees[connected_neighbors.value], connected_neighbors)

        # Second pass. re-base all labeling with representative label for each connected tree
        layers = {}
        for x in range(swt.shape[1]):
            for y in range(swt.shape[0]):
                if label_map[y, x] > 0:
                    item = disjointSet.labelSets[label_map[y, x]]
                    common_label = disjointSet.Find(item).value
                    label_map[y, x] = common_label
                    try:
                        layer = layers[common_label]
                    except KeyError:
                        layers[common_label] = np.zeros(shape=swt.shape, dtype=np.uint16)
                        layer = layers[common_label]

                    layer[y, x] = 1

        return layers


    def _find_letters(self, swt, shapes):
        # STEP: Discard shapes that are probably not letters
        swts = []
        heights = []
        widths = []
        topleft_pts = []
        images = []

        for label,layer in shapes.items():
            (nz_y, nz_x) = np.nonzero(layer)
            east, west, south, north = max(nz_x), min(nz_x), max(nz_y), min(nz_y)
            width, height = east - west, south - north

            if width < 10 or height < 10:
                continue

            # Aspect ratio checking (in the paper is between values 0.1 and 10)
            if width / height < 0.1 and width / height > 10:
                continue

            diameter = math.sqrt(width * width + height * height)
            median_swt = np.median(swt[(nz_y, nz_x)])
            if diameter / median_swt > 10:
                continue

            if width / layer.shape[1] > 0.4 or height / layer.shape[0] > 0.4:
                continue

            # we use log_base_2 so we can do linear distance comparison later using k-d tree
            # ie, if log2(x) - log2(y) > 1, we know that x > 2*y
            # Assumption: we've eliminated anything with median_swt == 1
            swts.append([math.log(median_swt, 2)])
            heights.append([math.log(height, 2)])
            topleft_pts.append(np.asarray([north, west]))
            widths.append(width)
            images.append(layer)

        return swts, heights, widths, topleft_pts, images


    def _find_words(self, swts, heights, widths, topleft_pts, images):
        # Find all shape pairs that have similar median stroke widths
        swt_tree = scipy.spatial.KDTree(np.asarray(swts))
        stp = swt_tree.query_pairs(1)

        # Find all shape pairs that have similar heights
        height_tree = scipy.spatial.KDTree(np.asarray(heights))
        htp = height_tree.query_pairs(1)

        # Intersection of valid pairings
        isect = htp.intersection(stp)

        chains = []
        pairs = []
        pair_angles = []
        for pair in isect:
            left = pair[0]
            right = pair[1]
            widest = max(widths[left], widths[right])
            distance = np.linalg.norm(topleft_pts[left] - topleft_pts[right])
            if distance < widest * 3:
                delta_yx = topleft_pts[left] - topleft_pts[right]
                angle = np.arctan2(delta_yx[0], delta_yx[1])
                if angle < 0:
                    angle += np.pi

                pairs.append(pair)
                pair_angles.append(np.asarray([angle]))

        angle_tree = scipy.spatial.KDTree(np.asarray(pair_angles))
        atp = angle_tree.query_pairs(np.pi/12)

        for pair_idx in atp:
            pair_a = pairs[pair_idx[0]]
            pair_b = pairs[pair_idx[1]]
            left_a = pair_a[0]
            right_a = pair_a[1]
            left_b = pair_b[0]
            right_b = pair_b[1]

            # @todo - this is O(n^2) or similar, extremely naive. Use a search tree.
            added = False
            for chain in chains:
                if left_a in chain:
                    chain.add(right_a)
                    added = True
                elif right_a in chain:
                    chain.add(left_a)
                    added = True
            if not added:
                chains.append(set([left_a, right_a]))
            added = False
            for chain in chains:
                if left_b in chain:
                    chain.add(right_b)
                    added = True
                elif right_b in chain:
                    chain.add(left_b)
                    added = True
            if not added:
                chains.append(set([left_b, right_b]))

        word_images = []
        for chain in [c for c in chains if len(c) > 3]:
            for idx in chain:
                word_images.append(images[idx])

        return word_images


if __name__ == '__main__':
    t0 = time.clock()
    outputPath = os.path.join(os.path.dirname(__file__), 'test/swt');
    local_filename = os.path.join(os.path.dirname(__file__), 'test/input/GoldenSpoon.jpg');
    img = cv.imread(local_filename, cv.IMREAD_GRAYSCALE);
    blurred = cv.GaussianBlur(img, (5, 5), 0);
    swt = SWTScrubber();
    final_mask = swt.scrub(blurred)
    resultImage = final_mask * 255;
    print("Time taken: {}".format(time.clock() - t0));
    cv.imwrite('{}/final.jpg'.format(outputPath), resultImage);

