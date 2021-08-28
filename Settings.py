from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, \
                            QMainWindow, \
                            QSystemTrayIcon, \
                            QAction, \
                            qApp, \
                            QMenu, \
                            QDesktopWidget

from auto_generated_UI import settigsUi

def center(window):
    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())


def start_settings_constr(app, size, window_to_hide):
    def start_settings(self):
        app.settings = Settings(width=size["settings_window_w"],
                            height=size["settings_window_h"])
        app.settings.show()
        window_to_hide.hide()
    return start_settings

class Settings(QMainWindow, settigsUi.Ui_Settings):
    def __init__(self, width=1280, height=720, x=0.5, y=0):
        super().__init__()

        self.setupUi(self)

        self.setFixedSize(width, height)
        if isinstance(x, float):
            center(self)
        else:
            self.move(x, y)

        self.setWindowTitle("Settings")
        self.setStyleSheet("QMainWindow{background-color: black;border: 1px solid white}")
        # self.setWindowFlags()

    # def closeEvent(self, event):
    # TODO disable hotkeys when in settings
