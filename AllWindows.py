from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, \
                            QMainWindow, \
                            QSystemTrayIcon, \
                            QAction, \
                            qApp, \
                            QMenu, \
                            QDesktopWidget


def center(window):
    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())


class Main(QMainWindow):
    def __init__(self, app: QApplication, width=1800, height=600, x=60, y=0):
        super().__init__()

        self.setFixedSize(width, height)
        self.move(x, y)
        self.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

        self.setFocusPolicy(Qt.StrongFocus)

        app.focusChanged.connect(self.on_focus_change)

        self.configure_tray()

    def on_focus_change(self):
        print(self.hasFocus())
        if not self.isActiveWindow():
            self.hide()

    def show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.setFocus()

    def start_settings(self):
        self.settings = Settings()
        self.settings.show()
        self.hide()

    def tray_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_hide()

    def configure_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("DropDownLogo_gray.png"))  # TODO Create icon

        show_hide_action = QAction("Show / Hide", self)
        settings_action = QAction("Settings", self)
        quit_action = QAction("Exit", self)

        show_hide_action.triggered.connect(self.show_hide)
        settings_action.triggered.connect(self.start_settings)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_hide_action)
        tray_menu.addAction(settings_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.activated.connect(self.tray_click)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()


class Settings(QMainWindow):
    def __init__(self, width=1280, height=720, x=0.5, y=0):
        super().__init__()

        self.setFixedSize(width, height)
        if isinstance(x, float):
            center(self)
        else:
            self.move(x, y)

        self.setWindowTitle("Settings")
        self.setStyleSheet("QMainWindow{background-color: black;border: 1px solid white}")
        # self.setWindowFlags()

    # def closeEvent(self, event):

