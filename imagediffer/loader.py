from scipy import misc
import requests

from .utils import norm_color


def load_image_from_file(file):
    return norm_color(misc.imread(file))


def load_image_from_url(url):
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise ValueError('Invalid image URL')

    return load_image_from_file(response.raw)
