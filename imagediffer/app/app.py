from PyQt5 import QtWidgets, uic

from .config import PATH_UI_MAINWINDOW


class App:
    def __init__(self):
        self.app = QtWidgets.QApplication([])
        self._init_window()

    def _init_window(self):
        self.window = QtWidgets.QMainWindow()
        with open(PATH_UI_MAINWINDOW) as f:
            uic.loadUi(f, self.window)

    def run(self):
        self.window.show()
        return self.app.exec_()
