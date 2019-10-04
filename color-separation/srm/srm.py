#! /usr/bin/env python
# PYTHON 2.7 CODE

import sys
import scipy
from matplotlib import pyplot
import cv2

from SRM import SRM

im = cv2.imread(sys.argv[2])
im = cv2.resize(im, (400, 400))
q = sys.argv[1]

srm = SRM(im, q)
segmented = srm.run()
cv2.imwrite('outputs/output-{}.jpg'.format(q), segmented)

pyplot.imshow(segmented/256)
pyplot.show()
