import os
import shutil

import numpy as np
import pytest

from imagediffer.core.loader import load_image_from_file, load_image_from_url, save_image


@pytest.yield_fixture
def temp_dir():
    tmp_path = 'tmp'
    os.mkdir(tmp_path)
    yield tmp_path
    shutil.rmtree(tmp_path)


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


def test_save_image(temp_dir):
    img = np.array([[[1., 0., 0., 1.], [1., 1., 1., 1.]],
                    [[1., 1., 1., 1.], [1., 0., 0., 1.]]])
    image_path = temp_dir + '/img.png'
    save_image(img, image_path)
    assert os.path.exists(image_path)


def test_save_image_without_extension(temp_dir):
    img = np.array([[[1., 0., 0., 1.], [1., 1., 1., 1.]],
                    [[1., 1., 1., 1.], [1., 0., 0., 1.]]])
    image_path = temp_dir + '/img'
    save_image(img, image_path)
    assert os.path.exists(image_path + '.png')
