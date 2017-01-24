from scipy import misc
import requests


def load_image_from_file(file):
    return misc.imread(file)


def load_image_from_url(url):
    response = requests.get(url, stream=True)

    if response.status_code != 200:
        raise ValueError('Invalid image URL')

    return misc.imread(response.raw)
