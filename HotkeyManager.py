from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtGui import QKeySequence
from pyqtkeybind import keybinder

class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, key_binder):
        self.keybinder = key_binder
        super().__init__()

    def nativeEventFilter(self, event_type, message):
        ret = self.keybinder.handler(event_type, message)
        return ret, 0


class HotkeyManager():
    def __init__(self,app):
        self.app = app
        keybinder.init()

    def add_hotkey(self,key_seq: QKeySequence):
        keybinder.register_hotkey(self.app.drop_menu_window.winId(), key_seq.toString(), self.app.drop_menu_window.show_hide)

        win_event_filter = WinEventFilter(keybinder)
        event_dispatcher = QAbstractEventDispatcher.instance()
        event_dispatcher.installNativeEventFilter(win_event_filter)

    def rem_hotkey(self,key_seq: QKeySequence):
        keybinder.unregister_hotkey(self.app.drop_menu_window.winId(), key_seq.toString())

