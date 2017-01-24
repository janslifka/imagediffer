import numpy as np


def norm_color(image):
    return image / 255


def extract_colors(image):
    return [norm_color(image[:, :, x]) for x in range(3)]


def to_grayscale(image):
    r, g, b = extract_colors(image)
    l = r * 299. / 1000 + g * 587. / 1000 + b * 114. / 1000
    return


def to_channel(source, index):
    image = np.empty(source.shape)
    for i in range(3):
        image[:, :, i] = source[:, :, index]
    return image


def to_red(img):
    image = np.copy(img)
    image[:, :, 1] = image[:, :, 0]
    image[:, :, 2] = image[:, :, 0]
    return image


def to_green(img):
    image = np.copy(img)
    image[:, :, 0] = image[:, :, 1]
    image[:, :, 2] = image[:, :, 1]
    return image


def to_blue(img):
    image = np.copy(img)
    image[:, :, 0] = image[:, :, 2]
    image[:, :, 1] = image[:, :, 2]
    return image
