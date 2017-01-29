import numpy as np


def norm_color(image):
    return image / 255


def extract_colors(image):
    return [image[:, :, x] for x in range(4)]


def to_red(source):
    image = np.copy(source)
    image[:, :, 1] = image[:, :, 0]
    image[:, :, 2] = image[:, :, 0]
    return image


def to_green(source):
    image = np.copy(source)
    image[:, :, 0] = image[:, :, 1]
    image[:, :, 2] = image[:, :, 1]
    return image


def to_blue(source):
    image = np.copy(source)
    image[:, :, 0] = image[:, :, 2]
    image[:, :, 1] = image[:, :, 2]
    return image


def to_grayscale(source):
    r, g, b, _ = extract_colors(source)
    l = r * 299. / 1000 + g * 587. / 1000 + b * 114. / 1000
    image = np.copy(source)
    for i in range(3):
        image[:, :, i] = l
    return image
