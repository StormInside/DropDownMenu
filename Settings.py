from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtCore import QSettings

from auto_generated_UI import settigsUi


def center(window):
    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())


def start_settings_constr(app, size, window_to_hide):
    def start_settings(self):
        app.settings = Settings()
        app.settings.show()
        window_to_hide.hide()
    return start_settings


class Settings(QMainWindow, settigsUi.Ui_Settings):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        settings = QSettings()
        settings.beginGroup("Screen")
        self.resize(settings.value("sett_frame_geometry").toSize())
        if settings.value("sett_pos") == "Center":
            center(self)
        else:
            self.move(settings.value("sett_pos").toPoint())
        settings.endGroup()
        self.settings = settings

        self.setWindowTitle("Settings")
        self.setStyleSheet("QMainWindow{background-color: black;border: 1px solid white}")

        self.hotkey_input.keySequenceChanged.connect(self._change_key_sequence)
        # self.setWindowFlags()

    def _change_key_sequence(self, new_key_seq: QKeySequence):
        print(new_key_seq.toString())
        mod_key_seq = QKeySequence((new_key_seq.toString()).split(',')[0].strip())
        self.hotkey_input.setKeySequence(mod_key_seq)
        # update_settings() #TODO

    # TODO disable hotkeys when in settings

