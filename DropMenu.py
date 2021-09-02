from PyQt5.QtCore import Qt, QSettings
from PyQt5.QtWidgets import QApplication, \
                            QMainWindow, \
                            QVBoxLayout, \
                            QSizeGrip

from auto_generated_UI import mainUi


class DropMenu(QMainWindow, mainUi.Ui_MainWindow):
    def __init__(self, app: QApplication):
        super().__init__()

        self.app = app
        self.setupUi(self)

        settings = QSettings()
        settings.beginGroup("Screen")
        size = settings.value("main_frame_geometry")
        pos = settings.value("main_pos")
        self.resize(size)
        self.move(pos)
        settings.endGroup()
        self.settings = settings

        self.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

        self.setFocusPolicy(Qt.NoFocus)
        self.app.focusChanged.connect(self.on_focus_change)

        layout = QVBoxLayout()
        sizegrip = QSizeGrip(self)
        layout.addWidget(sizegrip, 0, Qt.AlignBottom | Qt.AlignRight)
        self.setLayout(layout)

    def on_focus_change(self):
        # print(self.hasFocus())
        if not self.isActiveWindow():
            self.hide()

    def show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.setFocus()
            self.activateWindow()
