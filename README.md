# Image Differ

Image Differ is a tool for image comparison. It loads 2 images (either local files or from the internet) and generates the diff image that shows where the images are different. It also calculates:

- Percentage of pixels where the images differ (with adjustable threshold for difference)
- Mean Square Error for the images
- Structural Similarity Index
- Histogram for each image

It can also calculate comparison stats for individual color channels or ignore colors.

Image Differ can be used as a library for other projects or it provides GUI application.

## Used libraries

- [PyQt5](https://pypi.python.org/pypi/PyQt5)
- [NumPy](https://pypi.python.org/pypi/numpy/)
- [SciPy](https://pypi.python.org/pypi/scipy/)
- [matplotlib](https://pypi.python.org/pypi/matplotlib/)
- [requests](https://pypi.python.org/pypi/requests/)
- [Sphinx](https://pypi.python.org/pypi/Sphinx)
- [pytest](https://pypi.python.org/pypi/pytest)
