"""Loader module contains functions for loading and saving images.
"""
from os.path import splitext

import numpy as np
import requests
from PIL import Image
from scipy import misc

from .utils import norm_color


def load_image_from_file(file):
    """Load image as a numpy array from given file.

    :param file: Path to the image file
    :return: Numpy image array with color and alpha channels values from 0.0 to 1.0
    """
    return norm_color(misc.imread(file, mode='RGBA'))


def load_image_from_url(url):
    """Load image as a numpy array from given URL.

    :param url: Image URL
    :return: Numpy image array with color and alpha channels values from 0.0 to 1.0
    """
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise ValueError('Invalid image URL')

    return load_image_from_file(response.raw)


def save_image(image, path):
    """Save given image to the PNG file. If the file extension is not part of the ``path`` or is missing, it will be
    autocompleted or replaced.

    :param image: Numpy image array
    :param path: Path to the image file.
    """
    filename, extension = splitext(path)
    if extension != '.png':
        path = '{}{}'.format(filename, '.png')
    Image.fromarray((image * 255).astype(np.uint8), mode='RGBA').save(path)
