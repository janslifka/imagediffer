"""Differ module contains functions for comparing images and creating diff images
"""
import numpy as np
from PIL import Image
from ssim import compute_ssim

from .utils import extract_colors


def euclidean_distance(image1, image2):
    """Calculate `euclidean distance <https://en.wikipedia.org/wiki/Euclidean_distance>`_ for each pixel in ``image1``
    and ``image2``. Images must have same dimension.

    :param image1: Numpy image array
    :param image2: Numpy image array
    :return: Array of euclidean distances
    """
    r1, g1, b1, a1 = extract_colors(image1)
    r2, g2, b2, a2 = extract_colors(image2)
    return np.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2 + (a1 - a2) ** 2) / 2


def chebyshev_distance(image1, image2):
    """Calculate `chebyshev distance <https://en.wikipedia.org/wiki/Chebyshev_distance>`_ for each pixel in ``image1``
    and ``image2``. Images must have same dimension.

    :param image1: Numpy image array
    :param image2: Numpy image array
    :return: Array of chebyshev distances
    """
    r1, g1, b1, a1 = extract_colors(image1)
    r2, g2, b2, a2 = extract_colors(image2)
    return np.maximum(np.maximum(np.maximum(np.fabs(r1 - r2), np.fabs(g1 - g2)), np.fabs(b1 - b2)), np.fabs(a1 - a2))


def diff(image1, image2, compare_colors_method, tolerance=0, diff_color=(1., 0, 1., 1.)):
    """Create a diff image of ``image1`` and ``image2``. Pixels are considered different if the distance of colors is
    greater than ``tolerance`` using given ``compare_colors_method``. The result image is created by blending ``image1``
    and ``image2`` together and replacing different pixels with the ``diff_color``.

    :param image1: Numpy image array
    :param image2: Numpy image array
    :param compare_colors_method: Method that takes two numpy image arrays and return array of color distances in range from 0.0 to 1.0. You can use ``euclidean_distance``, ``chebyshev_distance`` or implement your own method.
    :param tolerance: Defines the color distance that is acceptable and colors are considered the same
    :param diff_color: RGBA color that should be used for different pixels
    :return:
       Tuple containing:
          - ``diff_image`` Numpy image array
          - ``diff_pctg`` Percentage of pixels where the color distance exceeded the acceptable tolerance
    """
    mask = compare_colors_method(image1, image2) > tolerance
    diff_pctg = mask[mask].size / mask.size
    diff_image = image1 * 0.5 + image2 * 0.5
    diff_image[mask] = diff_color
    return diff_image, diff_pctg


def calculate_mse(image1, image2):
    """Calculate `mean squared error <https://en.wikipedia.org/wiki/Mean_squared_error>`_ for given images. The higher
    the value of MSE is, the more different the images are.

    :param image1: Numpy image array
    :param image2: Numpy image array
    :return: Float number representing mean squared error
    """
    return np.sum((image1 - image2) ** 2) / float(image1.shape[0] * image1.shape[1])


def calculate_ssim(image1, image2):
    """Calculate `structural similarity index <https://en.wikipedia.org/wiki/Structural_similarity>`_ for given images.
    If the value is 1.0 the images are same. The lower the value is, the more different the images are.

    :param image1: Numpy image array
    :param image2: Numpy image array
    :return: Float number from -1.0 to 1.0 representing SSIM
    """
    return compute_ssim(
        Image.fromarray((image1[:, :, :3] * 255).astype(np.uint8), mode='RGB'),
        Image.fromarray((image2[:, :, :3] * 255).astype(np.uint8), mode='RGB')
    )
