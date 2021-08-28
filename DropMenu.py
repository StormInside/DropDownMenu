from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, \
                            QMainWindow, \
                            QVBoxLayout, \
                            QSizeGrip

from auto_generated_UI import mainUi


class DropMenu(QMainWindow, mainUi.Ui_MainWindow):
    def __init__(self, app: QApplication,
                 width=1800,
                 height=600,
                 x=60,
                 y=0):
        super().__init__()

        # self.setFixedSize(width, height)
        self.move(x, y)
        self.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

        self.setFocusPolicy(Qt.NoFocus)

        app.focusChanged.connect(self.on_focus_change)

        self.setupUi(self)

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
