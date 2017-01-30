"""Utils module contains various functions for manipulating images.
"""
import numpy as np


def norm_color(image):
    """Normalize colors to be in range from 0.0 to 1.0 instead of from 0 to 255.

    :param image: Numpy image array with colors from 0 to 255

    :return: Numpy image array with colors normalized to floats
    """
    return image / 255


def extract_colors(image):
    """Extract individual color channels and alpha channel from numpy image array.

    :param image: Numpy image array
    :return: Array of width × height numpy arrays for each color and alpha channels
    """
    return [image[:, :, x] for x in range(4)]


def to_red(source):
    """Convert source image to image using red channel for all color channels.

    :param source: Numpy image array
    :return: Numpy image array
    """
    image = np.copy(source)
    image[:, :, 1] = image[:, :, 0]
    image[:, :, 2] = image[:, :, 0]
    return image


def to_green(source):
    """Convert source image to image using green channel for all color channels.

    :param source: Numpy image array
    :return: Numpy image array
    """
    image = np.copy(source)
    image[:, :, 0] = image[:, :, 1]
    image[:, :, 2] = image[:, :, 1]
    return image


def to_blue(source):
    """Convert source image to image using blue channel for all color channels.

    :param source: Numpy image array
    :return: Numpy image array
    """
    image = np.copy(source)
    image[:, :, 0] = image[:, :, 2]
    image[:, :, 1] = image[:, :, 2]
    return image


def to_grayscale(source):
    """
    Convert image to grayscale using `PAL/NTSC conversion
    <https://en.wikipedia.org/wiki/Grayscale#Luma_coding_in_video_systems>`_.

    :param source: Numpy image array
    :return: Numpy image array
    """
    r, g, b, _ = extract_colors(source)
    l = r * .299 + g * .587 + b * .114
    image = np.copy(source)
    for i in range(3):
        image[:, :, i] = l
    return image
