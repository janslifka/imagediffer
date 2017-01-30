Image Differ
============

.. image:: https://readthedocs.org/projects/imagediffer/badge/?version=latest
   :target: http://imagediffer.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Image Differ is a tool for image comparison. It loads 2 images (either local files or from the internet) and generates the diff image that shows where the images are different. It also calculates:

- Percentage of pixels where the images differ (with adjustable threshold for difference)
- Mean Square Error for the images
- Structural Similarity Index

It can also calculate comparison stats for individual color channels or convert images to grayscale.

Image Differ can be used as a library for other projects or it provides GUI application.


Used libraries
--------------

- `NumPy <https://pypi.python.org/pypi/numpy>`_
- `Pillow <https://pypi.python.org/pypi/Pillow>`_
- `PyQt5 <https://pypi.python.org/pypi/PyQt5>`_
- `pyssim <https://pypi.python.org/pypi/pyssim>`_
- `pytest <https://pypi.python.org/pypi/pytest>`_
- `requests <https://pypi.python.org/pypi/requests>`_
- `SciPy <https://pypi.python.org/pypi/scipy>`_
- `Sphinx <https://pypi.python.org/pypi/Sphinx>`_
