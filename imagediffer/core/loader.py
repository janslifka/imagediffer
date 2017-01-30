from os.path import splitext

import numpy as np
import requests
from PIL import Image
from scipy import misc

from .utils import norm_color


def load_image_from_file(file):
    return norm_color(misc.imread(file, mode='RGBA'))


def load_image_from_url(url):
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise ValueError('Invalid image URL')

    return load_image_from_file(response.raw)


def save_image(image, path):
    filename, extension = splitext(path)
    if extension != '.png':
        path = '{}{}'.format(filename, '.png')
    Image.fromarray((image * 255).astype(np.uint8), mode='RGBA').save(path)
