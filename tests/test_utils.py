import numpy as np
import pytest

from imagediffer.core.loader import load_image_from_file
from imagediffer.core.utils import norm_color, extract_colors, to_red, to_green, to_blue, to_grayscale


@pytest.fixture
def image_checker_red_white():
    return load_image_from_file('tests/fixtures/checker-red-white.png')


@pytest.fixture
def image_checker_colors():
    return load_image_from_file('tests/fixtures/checker-colors.png')


def test_norm_color():
    image = np.array([[[255, 0, 0, 255], [255, 255, 255, 255]],
                      [[255, 255, 255, 255], [255, 0, 0, 255]]])
    ref = [[[1., 0., 0., 1.], [1., 1., 1., 1.]],
           [[1., 1., 1., 1.], [1., 0., 0., 1.]]]
    normalized = norm_color(image)
    assert np.array_equal(normalized, ref)


def test_extract_colors(image_checker_colors):
    ref_r = [[1., 0.], [1., 0.]]
    ref_g = [[0., 1.], [1., 0.]]
    ref_b = [[0., 0.], [1., 1.]]
    ref_a = [[1., 1.], [1., 1.]]

    r, g, b, a = extract_colors(image_checker_colors)

    assert np.array_equal(r, ref_r)
    assert np.array_equal(g, ref_g)
    assert np.array_equal(b, ref_b)
    assert np.array_equal(a, ref_a)


def test_to_red(image_checker_colors):
    ref = [[[1., 1., 1., 1.], [0., 0., 0., 1.]],
           [[1., 1., 1., 1.], [0., 0., 0., 1.]]]
    red = to_red(image_checker_colors)
    assert np.array_equal(red, ref)


def test_to_green(image_checker_colors):
    ref = [[[0., 0., 0., 1.], [1., 1., 1., 1.]],
           [[1., 1., 1., 1.], [0., 0., 0., 1.]]]
    green = to_green(image_checker_colors)
    assert np.array_equal(green, ref)


def test_to_blue(image_checker_colors):
    ref = [[[0., 0., 0., 1.], [0., 0., 0., 1.]],
           [[1., 1., 1., 1.], [1., 1., 1., 1.]]]
    blue = to_blue(image_checker_colors)
    assert np.array_equal(blue, ref)


def test_to_grayscale(image_checker_colors):
    ref = [
        [
            [1. * 299. / 1000, 1. * 299. / 1000, 1. * 299. / 1000, 1.],
            [1. * 587. / 1000, 1. * 587. / 1000, 1. * 587. / 1000, 1.]
        ], [
            [1., 1., 1., 1.],
            [1. * 114. / 1000, 1. * 114. / 1000, 1. * 114. / 1000, 1.]
        ]
    ]

    grayscale = to_grayscale(image_checker_colors)
    assert np.all(np.isclose(grayscale, ref))
