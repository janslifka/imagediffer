import numpy as np
from PyQt5 import QtWidgets, QtGui, uic

from ..core.differ import calculate_mse, calculate_ssim, chebyshev_distance, euclidean_distance, diff
from ..core.loader import load_image_from_file, load_image_from_url, save_image

from .config import PATH_UI_MAINWINDOW, PATH_UI_OPEN_IMAGE
from .image_struct import ImageStruct


COLOR_MODES = ['colors', 'grayscale', 'red', 'blue', 'green']


class App:
    """PyQt5 application for using core library.

    To run the application, simply create an instance and call run method.

    .. code-block:: python

       from imagediffer.app.app import App

       App().run()
    """
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
        self._init_scroll_areas()
        self._init_menu_actions()

        self._first_image = ImageStruct()
        self._second_image = ImageStruct()
        self._diff = None

    def run(self):
        """Run the application.
        """
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

    def _init_scroll_areas(self):
        self._first_image_scroll_area = self._window.findChild(QtWidgets.QScrollArea, 'first_image_scroll_area')
        self._diff_image_scroll_area = self._window.findChild(QtWidgets.QScrollArea, 'diff_image_scroll_area')
        self._second_image_scroll_area = self._window.findChild(QtWidgets.QScrollArea, 'second_image_scroll_area')

    def _init_menu_actions(self):
        action = self._window.findChild(QtWidgets.QAction, 'action_load_first_image_from_file')
        action.triggered.connect(lambda: self._load_first_image_from_file())

        action = self._window.findChild(QtWidgets.QAction, 'action_load_second_image_from_file')
        action.triggered.connect(lambda: self._load_second_image_from_file())

        action = self._window.findChild(QtWidgets.QAction, 'action_load_first_image_from_URL')
        action.triggered.connect(lambda: self._load_first_image_from_url())

        action = self._window.findChild(QtWidgets.QAction, 'action_load_second_image_from_URL')
        action.triggered.connect(lambda: self._load_second_image_from_url())

        self._save_action = self._window.findChild(QtWidgets.QAction, 'action_save_diff_image')
        self._save_action.triggered.connect(lambda: self._save_diff_image())

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
        self._tolerance = self._tolerance_slider.value() / 100.
        self._compare_images()

    def _compare_images(self):
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

        if image1 is not None:
            self._show_image(self._first_image_scroll_area, image1)

        if image2 is not None:
            self._show_image(self._second_image_scroll_area, image2)

        if image1 is not None and image2 is not None:
            if image1.shape == image2.shape:
                self._diff, pctg = diff(image1, image2, self._comparison_method, self._tolerance)
                self._show_image(self._diff_image_scroll_area, self._diff)
                self._mismatch_value.setText('{}%'.format(round(pctg * 100, 2)))
                self._mse_value.setText('{}'.format(round(calculate_mse(image1, image2), 2)))
                self._ssim_value.setText('{}'.format(round(calculate_ssim(image1, image2), 2)))
                self._save_action.setEnabled(True)
            else:
                self._show_shape_not_match()
                self._mismatch_value.setText('-')
                self._mse_value.setText('-')
                self._ssim_value.setText('-')
                self._save_action.setEnabled(False)

    def _show_image(self, scroll_area, image):
        image = (image * 255).astype(np.uint8)
        img = QtGui.QImage(image, image.shape[1], image.shape[0], image.shape[1] * 4, QtGui.QImage.Format_RGBA8888)
        image_label = QtWidgets.QLabel()
        image_label.setPixmap(QtGui.QPixmap(img))
        scroll_area.setWidget(image_label)

    def _show_shape_not_match(self):
        label = QtWidgets.QLabel()
        label.setText('Images have different sizes.')
        self._diff_image_scroll_area.setWidget(label)

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

    def _save_diff_image(self):
        file_name = QtWidgets.QFileDialog.getSaveFileName(self._window)
        if len(file_name[0]) > 0:
            save_image(self._diff, file_name[0])
