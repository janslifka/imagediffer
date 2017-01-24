import numpy as np
import math

from .utils import extract_colors


def euclidean_distance(image1, image2):
    r1, g1, b1 = extract_colors(image1)
    r2, g2, b2 = extract_colors(image2)
    return np.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) / math.sqrt(3)


def chebyshev_distance(image1, image2):
    r1, g1, b1 = extract_colors(image1)
    r2, g2, b2 = extract_colors(image2)
    return np.maximum(np.fabs(r1 - r2), np.fabs(g1 - g2), np.fabs(b1 - b2))


def diff(image1, image2, compare_colors_method, tolerance=0, diff_color=(255, 0, 255)):
    mask = compare_colors_method(image1, image2) > tolerance
    diff_pctg = mask[mask].size / mask.size
    diff_image = np.copy(image1)
    diff_image[mask] = diff_color
    return diff_image, diff_pctg
