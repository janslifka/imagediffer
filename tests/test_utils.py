import pytest
import numpy as np

from imagediffer.loader import load_image_from_file
from imagediffer.utils import norm_color, extract_colors, to_red, to_green, to_blue, to_grayscale


@pytest.fixture
def image_checker_red_white():
    return load_image_from_file('tests/fixtures/checker-red-white.png')


@pytest.fixture
def image_checker_colors():
    return load_image_from_file('tests/fixtures/checker-colors.png')


def test_norm_color(image_checker_red_white):
    ref = [[[1., 0., 0.], [1., 1., 1.]],
           [[1., 1., 1.], [1., 0., 0.]]]
    normalized = norm_color(image_checker_red_white)
    assert np.array_equal(normalized, ref)


def test_extract_colors(image_checker_colors):
    ref_r = [[255, 0], [255, 0]]
    ref_g = [[0, 255], [255, 0]]
    ref_b = [[0, 0], [255, 255]]

    r, g, b = extract_colors(image_checker_colors)

    assert np.array_equal(r, ref_r)
    assert np.array_equal(g, ref_g)
    assert np.array_equal(b, ref_b)


def test_to_red(image_checker_colors):
    ref = [[[255, 255, 255], [0, 0, 0]],
           [[255, 255, 255], [0, 0, 0]]]
    red = to_red(image_checker_colors)
    assert np.array_equal(red, ref)


def test_to_green(image_checker_colors):
    ref = [[[0, 0, 0], [255, 255, 255]],
           [[255, 255, 255], [0, 0, 0]]]
    green = to_green(image_checker_colors)
    assert np.array_equal(green, ref)


def test_to_blue(image_checker_colors):
    ref = [[[0, 0, 0], [0, 0, 0]],
           [[255, 255, 255], [255, 255, 255]]]
    blue = to_blue(image_checker_colors)
    assert np.array_equal(blue, ref)


def test_to_grayscale(image_checker_colors):
    ref = [
        [
            [255 * 299. / 1000, 255 * 299. / 1000, 255 * 299. / 1000],
            [255 * 587. / 1000, 255 * 587. / 1000, 255 * 587. / 1000]
        ], [
            [255, 255, 255],
            [255 * 114. / 1000, 255 * 114. / 1000, 255 * 114. / 1000]
        ]
    ]

    grayscale = to_grayscale(image_checker_colors)
    assert np.array_equal(grayscale, ref)

