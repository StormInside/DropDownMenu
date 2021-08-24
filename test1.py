import sys
from PyQt5.QtCore import Qt, QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtWidgets import QApplication, \
                            QMainWindow, \
                            QSystemTrayIcon, \
                            QStyle, \
                            QAction, \
                            qApp, \
                            QMenu

from pyqtkeybind import keybinder


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


class Main(QMainWindow):
    def __init__(self, app: QApplication, width=1800, height=600, x=60, y=0):
        super().__init__()

        self.setFixedSize(width, height)
        self.move(x, y)
        self.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)  # TODO Create icon

        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(self.style().standardIcon(QStyle.SP_ComputerIcon))

        show_hide_action = QAction("Show / Hide", self)
        quit_action = QAction("Exit", self)

        show_hide_action.triggered.connect(self.show_hide)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_hide_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

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


def run():
    app = QApplication(sys.argv)
    window = Main(app)

    keybinder.init()
    unregistered = False

    def show_hide():
        window.show_hide()

    keybinder.register_hotkey(window.winId(), "Shift+Ctrl+A", show_hide)

    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    window.show()

    app.exec_()
    keybinder.unregister_hotkey(window.winId(), "Shift+Ctrl+A")

if __name__ == '__main__':

    sys.exit(run())



