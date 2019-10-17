import cv2
import math
import numpy as np


def apply_mask(matrix, mask, fill_value):
    masked = np.ma.array(matrix, mask=mask, fill_value=fill_value)
    return masked.filled()


def apply_threshold(matrix, low_value, high_value):
    low_mask = matrix < low_value
    matrix = apply_mask(matrix, low_mask, low_value)

    high_mask = matrix > high_value
    matrix = apply_mask(matrix, high_mask, high_value)

    return matrix


def simpleColorBalance(img, percent=1):
    assert img.shape[2] == 3
    assert percent > 0 and percent < 100

    half_percent = percent / 200.0

    channels = cv2.split(img)

    out_channels = []
    for channel in channels:
        assert len(channel.shape) == 2
        # find the low and high precentile values (based on the input percentile)
        height, width = channel.shape
        vec_size = width * height
        flat = channel.reshape(vec_size)

        assert len(flat.shape) == 1

        flat = np.sort(flat)

        n_cols = flat.shape[0]

        low_val = flat[math.floor(n_cols * half_percent)]
        high_val = flat[math.ceil(n_cols * (1.0 - half_percent))]

        # saturate below the low percentile and above the high percentile
        thresholded = apply_threshold(channel, low_val, high_val)
        # scale the channel
        normalized = cv2.normalize(
            thresholded, thresholded.copy(), 0, 255, cv2.NORM_MINMAX)
        out_channels.append(normalized)

    return cv2.merge(out_channels)


def invert(image):
    return (255-image)


def RGB2CMYK(rgb):
    r_p = rgb[0]/255
    g_p = rgb[1]/255
    b_p = rgb[2]/255
    k = 1 - max(r_p, g_p, b_p)
    if float(k) == 1.0:
        return (0, 0, 0, 100)
    c = round((max(1 - r_p - k, 0) / (1 - k)) * 100)
    m = round((max(1 - g_p - k, 0) / (1 - k)) * 100)
    y = round((max(1 - b_p - k, 0) / (1 - k)) * 100)
    k = round(k * 100)
    return (c, m, y, k)


def CMYK2RGB(cmyk):
    c = cmyk[0]
    m = cmyk[1]
    y = cmyk[2]
    k = cmyk[3]
    r = round(255 * (1 - (c / 100)) * (1 - (k / 100)))
    g = round(255 * (1 - (m / 100)) * (1 - (k / 100)))
    b = round(255 * (1 - (y / 100)) * (1 - (k / 100)))
    return (r, g, b)
