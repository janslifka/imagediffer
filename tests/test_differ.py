import math

import numpy as np
import pytest

from imagediffer.core.loader import load_image_from_file
from imagediffer.core.differ import euclidean_distance, chebyshev_distance, diff


def load_test_image(name):
    return load_image_from_file('tests/fixtures/{}.png'.format(name))


@pytest.mark.parametrize('image1,image2,ref', [
    (
        [[[1., 1., 1., 1.], [0., 0., 0., 0.]]],
        [[[0., 0., 0., 0.], [1., 1., 1., 1.]]],
        [[1., 1.]]
    ), (
        [[[1., 0., 0., 1.], [1., 1., 0, 1.]]],
        [[[0., 0., 0., 1.], [0., 0., 0, 1.]]],
        [[math.sqrt(1. / 4), math.sqrt(2. / 4)]]
    ), (
        [[[1., .5, 0., 1.], [1., 1., 0, 1.]]],
        [[[0., .5, 1., 1.], [0., 1., .5, 1.]]],
        [[math.sqrt(2. / 4), math.sqrt(1.25 / 4)]]
    )
])
def test_euclidean_distance(image1, image2, ref):
    image1 = np.array(image1)
    image2 = np.array(image2)
    ref = np.array(ref)
    distances = euclidean_distance(image1, image2)
    assert np.all(np.isclose(distances, ref))


@pytest.mark.parametrize('image1,image2,ref', [
    (
        [[[1., 1., 1., 1.], [0., 0., 0., 1.]]],
        [[[0., 0., 0., 1.], [1., 1., 1., 1.]]],
        [[1., 1.]]
    ), (
        [[[.6, .4, .2, 1.], [.8, .5, .2, 1.]]],
        [[[0., 0., 0., 1.], [1., 1., 1., 1.]]],
        [[.6, .8]]
    ), (
        [[[.12, .32, .23, 1.], [.37, .89, .98, 1.]]],
        [[[.45, .45, .73, 1.], [.34, .35, .78, 1.]]],
        [[.5, .54]]
    )
])
def test_chebyshev_distance(image1, image2, ref):
    image1 = np.array(image1)
    image2 = np.array(image2)
    ref = np.array(ref)
    distances = chebyshev_distance(image1, image2)
    assert np.all(np.isclose(distances, ref))


@pytest.mark.parametrize('image1,image2,diff_image,method,mismatch,tolerance,diff_color', [
    ('red', 'blue', 'diff_all', euclidean_distance, 1., 0., (1., 0, 1., 1.)),
    ('red', 'blue', 'diff_all', chebyshev_distance, 1., 0., (1., 0, 1., 1.)),
    ('red', 'light_red', 'diff_red_left', euclidean_distance, .5, 0., (1., 0, 1., 1.)),
    ('red', 'light_red', 'diff_red_left', chebyshev_distance, .5, 0., (1., 0, 1., 1.)),
    ('red', 'light_red', 'red_blended', euclidean_distance, 0., .3, (1., 0, 1., 1.)),
    ('red', 'light_red', 'red_blended', chebyshev_distance, 0., .3, (1., 0, 1., 1.)),
    ('red', 'light_red', 'diff_red_left_yellow', euclidean_distance, .5, 0., (1., 1., 0., 1.)),
    ('red', 'light_red', 'diff_red_left_yellow', chebyshev_distance, .5, 0., (1., 1., 0., 1.)),
])
def test_diff(image1, image2, diff_image, method, mismatch, tolerance, diff_color):
    image1 = load_test_image(image1)
    image2 = load_test_image(image2)
    diff_image = load_test_image(diff_image)
    result, pctg = diff(image1, image2, method, tolerance, diff_color)
    assert np.array_equal(result, diff_image)
    assert abs(pctg - mismatch) < 0.0001
