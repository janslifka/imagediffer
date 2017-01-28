import numpy as np
import pytest

from imagediffer.lib.loader import load_image_from_file, load_image_from_url


def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_image_from_file('tests/fixtures/unknown')


def test_load_from_file():
    ref = [[[1., 0., 0., 1.], [1., 1., 1., 1.]],
           [[1., 1., 1., 1.], [1., 0., 0., 1.]]]

    image = load_image_from_file('tests/fixtures/checker-red-white.png')
    assert np.array_equal(image, ref)


def test_invalid_url():
    with pytest.raises(ValueError):
        load_image_from_url('http://example.com/image.jpg')
