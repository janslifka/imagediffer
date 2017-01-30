from ..core.utils import to_grayscale, to_red, to_green, to_blue


class ImageStruct:
    def __init__(self):
        self._initialize()

    def _initialize(self):
        self._image = None
        self._colors = None
        self._grayscale = None
        self._red = None
        self._green = None
        self._blue = None

    @property
    def initialized(self):
        return self._image is not None

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._initialize()
        self._image = value

    @property
    def grayscale(self):
        if self.initialized and self._grayscale is None:
            self._grayscale = to_grayscale(self._image)
        return self._grayscale

    @property
    def red(self):
        if self.initialized and self._red is None:
            self._red = to_red(self._image)
        return self._red

    @property
    def green(self):
        if self.initialized and self._green is None:
            self._green = to_green(self._image)
        return self._green

    @property
    def blue(self):
        if self.initialized and self._blue is None:
            self._blue = to_blue(self._image)
        return self._blue
