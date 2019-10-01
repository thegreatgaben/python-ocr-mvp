import numpy as np
import cv2 as cv

def basicLinearTransform(image):
    '''
    Increase the contrast and brightness of the image in a linear manner
    '''
    alpha = 1.0 # Simple contrast control
    beta = 0    # Simple brightness control

    # Initialize values
    print(' Basic Linear Transforms ')
    print('-------------------------')
    try:
        alpha = float(input('* Enter the alpha value [1.0-3.0]: '))
        beta = int(input('* Enter the beta value [0-100]: '))
    except ValueError:
        print('Error, not a number')

    new_image = cv.convertScaleAbs(image, alpha=alpha, beta=beta)
    return new_image;


def gammaCorrection(image, gamma=0.25):
    ## [changing-contrast-brightness-gamma-correction]
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, gamma) * 255.0, 0, 255)

    res = cv.LUT(image, lookUpTable)
    return res

