import pytest
import numpy as np
import math

from imagediffer.differ import euclidean_distance, chebyshev_distance, diff


@pytest.mark.parametrize('image1,image2,ref', [
    (
        [[[1., 1., 1.], [0., 0., 0.]]],
        [[[0., 0., 0.], [1., 1., 1.]]],
        [[1., 1.]]
    ), (
        [[[1., 0., 0.], [1., 1., 0]]],
        [[[0., 0., 0.], [0., 0., 0]]],
        [[math.sqrt(1. / 3), math.sqrt(2. / 3)]]
    ), (
        [[[1., .5, 0.], [1., 1., 0]]],
        [[[0., .5, 1.], [0., 1., .5]]],
        [[math.sqrt(2. / 3), math.sqrt(1.25 / 3)]]
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
        [[[1., 1., 1.], [0., 0., 0.]]],
        [[[0., 0., 0.], [1., 1., 1.]]],
        [[1., 1.]]
    ), (
        [[[.6, .4, .2], [.8, .5, .2]]],
        [[[0., 0., 0.], [1., 1., 1.]]],
        [[.6, .8]]
    ), (
        [[[.12, .32, .23], [.37, .89, .98]]],
        [[[.45, .45, .73], [.34, .35, .78]]],
        [[.5, .54]]
    )
])
def test_chebyshev_distance(image1, image2, ref):
    image1 = np.array(image1)
    image2 = np.array(image2)
    ref = np.array(ref)
    distances = chebyshev_distance(image1, image2)
    assert np.all(np.isclose(distances, ref))
