import sys
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, \
                            QMainWindow, \
                            QSystemTrayIcon, \
                            QStyle, \
                            QAction, \
                            qApp, \
                            QMenu, \
                            QShortcut


class Main(QMainWindow):
    def __init__(self, width=1800, height=600, x=60, y=0):
        super().__init__()

        self.setFixedSize(width, height)
        self.move(x, y)
        self.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)  # TODO Create icon

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_action = QAction("Show", self)
        quit_action = QAction("Exit", self)
        hide_action = QAction("Hide", self)

        show_action.triggered.connect(self.show)
        hide_action.triggered.connect(self.hide)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        self.show_hide_key = QShortcut(QKeySequence('Ctrl+F'), self)
        self.show_hide_key.activated.connect(self.show_hide)

        self.show()

        self.setFocus()
        app.focusChanged.connect(self.on_focus_change)

    def on_focus_change(self):
        print(self.hasFocus())
        if not self.isActiveWindow():
            self.hide()

    def show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Main()
    sys.exit(app.exec_())
