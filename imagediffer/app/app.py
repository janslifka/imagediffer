from PyQt5 import QtWidgets, uic

from .config import PATH_UI_MAINWINDOW, PATH_UI_OPEN_IMAGE
from ..lib.differ import euclidean_distance, chebyshev_distance, diff
from ..lib.loader import load_image_from_file, load_image_from_url
from .image_struct import ImageStruct

COLOR_MODES = ['colors', 'grayscale', 'red', 'blue', 'green']


class App:
    def __init__(self):
        self._app = QtWidgets.QApplication([])

        self._comparison_method = euclidean_distance
        self._color_mode = 'colors'
        self._tolerance = 0.

        self._init_window()
        self._init_color_distance()
        self._init_tolerance()
        self._init_color_channels()
        self._init_stats()
        self._init_menu_actions()

        self._first_image = ImageStruct()
        self._second_image = ImageStruct()
        self._diff = None

    def run(self):
        self._window.show()
        return self._app.exec_()

    def _init_window(self):
        self._window = QtWidgets.QMainWindow()
        with open(PATH_UI_MAINWINDOW) as f:
            uic.loadUi(f, self._window)

    def _init_color_distance(self):
        euclidean = self._window.findChild(QtWidgets.QRadioButton, 'method_euclidean_radio')
        chebyshev = self._window.findChild(QtWidgets.QRadioButton, 'method_chebyshev_radio')

        euclidean.toggled.connect(self._set_method_euclidean)
        chebyshev.toggled.connect(self._set_method_chebyshev)

    def _init_tolerance(self):
        self._tolerance_slider = self._window.findChild(QtWidgets.QSlider, 'tolerance_slider')
        self._tolerance_slider.valueChanged.connect(self._tolerance_changed)

    def _init_color_channels(self):
        for mode in COLOR_MODES:
            radio = self._window.findChild(QtWidgets.QRadioButton, 'color_{}_radio'.format(mode))
            radio.toggled.connect(lambda enabled, current_mode=mode: self._set_color_mode(enabled, current_mode))

    def _init_stats(self):
        self._mismatch_value = self._window.findChild(QtWidgets.QLabel, 'mismatch_value_label')
        self._mse_value = self._window.findChild(QtWidgets.QLabel, 'mse_value_label')
        self._ssim_value = self._window.findChild(QtWidgets.QLabel, 'ssim_value_label')

    def _init_menu_actions(self):
        action = self._window.findChild(QtWidgets.QAction, 'action_load_first_image_from_file')
        action.triggered.connect(lambda: self._load_first_image_from_file())

        action = self._window.findChild(QtWidgets.QAction, 'action_load_second_image_from_file')
        action.triggered.connect(lambda: self._load_second_image_from_file())

        action = self._window.findChild(QtWidgets.QAction, 'action_load_first_image_from_URL')
        action.triggered.connect(lambda: self._load_first_image_from_url())

        action = self._window.findChild(QtWidgets.QAction, 'action_load_second_image_from_URL')
        action.triggered.connect(lambda: self._load_second_image_from_url())

    def _set_method_euclidean(self, enabled):
        if enabled:
            self._comparison_method = euclidean_distance
            self._compare_images()

    def _set_method_chebyshev(self, enabled):
        if enabled:
            self._comparison_method = chebyshev_distance
            self._compare_images()

    def _set_color_mode(self, enabled, mode):
        if enabled:
            self._color_mode = mode
            self._compare_images()

    def _tolerance_changed(self):
        self._tolerance = self._tolerance_slider.value()
        self._compare_images()

    def _compare_images(self):
        if self._first_image.initialized and self._second_image.initialized:
            self._create_diff()

    def _create_diff(self):
        if self._color_mode == 'grayscale':
            image1 = self._first_image.grayscale
            image2 = self._second_image.grayscale
        elif self._color_mode == 'red':
            image1 = self._first_image.red
            image2 = self._second_image.red
        elif self._color_mode == 'green':
            image1 = self._first_image.green
            image2 = self._second_image.green
        elif self._color_mode == 'blue':
            image1 = self._first_image.blue
            image2 = self._second_image.blue
        else:
            image1 = self._first_image.image
            image2 = self._second_image.image

        self._diff = diff(image1, image2, self._comparison_method, self._tolerance)

    def _load_first_image_from_file(self):
        image = self._load_image_from_file()
        if image is not None:
            self._first_image.image = image
            self._compare_images()

    def _load_second_image_from_file(self):
        image = self._load_image_from_file()
        if image is not None:
            self._second_image.image = image
            self._compare_images()

    def _load_first_image_from_url(self):
        image = self._load_image_from_url()
        if image is not None:
            self._first_image.image = image
            self._compare_images()

    def _load_second_image_from_url(self):
        image = self._load_image_from_url()
        if image is not None:
            self._second_image.image = image
            self._compare_images()

    def _load_image_from_file(self):
        file_name = QtWidgets.QFileDialog.getOpenFileName(self._window)
        if len(file_name[0]) > 0:
            try:
                image = load_image_from_file(file_name[0])
                return image
            except:
                QtWidgets.QMessageBox.critical(self._window, 'File error', 'Unable to open image from given file')
        return None

    def _load_image_from_url(self):
        dialog = QtWidgets.QDialog()
        with open(PATH_UI_OPEN_IMAGE) as f:
            uic.loadUi(f, dialog)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Rejected:
            return None

        url = dialog.findChild(QtWidgets.QLineEdit, 'url').text()

        try:
            image = load_image_from_url(url)
            return image
        except:
            QtWidgets.QMessageBox.critical(self._window, 'File error', 'Unable to open image from given URL')

        return None
