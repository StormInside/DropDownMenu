import sys
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtWidgets import QApplication

from pyqtkeybind import keybinder

import AllWindows


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, keybinder):
        self.keybinder = keybinder
        super().__init__()

    def nativeEventFilter(self, eventType, message):
        ret = self.keybinder.handler(eventType, message)
        return ret, 0


def run():
    app = QApplication(sys.argv)
    window = AllWindows.Main(app)

    keybinder.init()

    keybinder.register_hotkey(window.winId(), "Shift+Ctrl+A", window.show_hide)

    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    # window.show()

    app.exec_()
    keybinder.unregister_hotkey(window.winId(), "Shift+Ctrl+A")


if __name__ == '__main__':

    sys.exit(run())



