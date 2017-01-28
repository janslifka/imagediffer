from PyQt5 import QtWidgets, uic

from .config import PATH_UI_MAINWINDOW
from ..lib.differ import euclidean_distance, chebyshev_distance


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
        print('Compare images: \nmethod: {}\nmode: {}\ntolerance: {}\n'.format(self._comparison_method, self._color_mode, self._tolerance))
