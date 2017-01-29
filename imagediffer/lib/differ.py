import numpy as np
import math
from ssim import compute_ssim
from PIL import Image

from .utils import extract_colors


def euclidean_distance(image1, image2):
    r1, g1, b1, a1 = extract_colors(image1)
    r2, g2, b2, a2 = extract_colors(image2)
    return np.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2 + (a1 - a2) ** 2) / 2


def chebyshev_distance(image1, image2):
    r1, g1, b1, a1 = extract_colors(image1)
    r2, g2, b2, a2 = extract_colors(image2)
    return np.maximum(np.maximum(np.maximum(np.fabs(r1 - r2), np.fabs(g1 - g2)), np.fabs(b1 - b2)), np.fabs(a1 - a2))


def diff(image1, image2, compare_colors_method, tolerance=0, diff_color=(1, 0, 1, 1)):
    mask = compare_colors_method(image1, image2) > tolerance
    diff_pctg = mask[mask].size / mask.size
    diff_image = image1 * 0.5 + image2 * 0.5
    diff_image[mask] = diff_color
    return diff_image, diff_pctg


def calculate_mse(image1, image2):
    return np.sum((image1 - image2) ** 2) / float(image1.shape[0] * image1.shape[1])


def calculate_ssim(image1, image2):
    return compute_ssim(
        Image.fromarray((image1[:, :, :3] * 255).astype(np.uint8), mode='RGB'),
        Image.fromarray((image2[:, :, :3] * 255).astype(np.uint8), mode='RGB')
    )
