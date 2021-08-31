import sys
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher, Qt, QSettings
from PyQt5.QtWidgets import QApplication

from pyqtkeybind import keybinder

import DropMenu
import Settings
import Tray
import InitialConfig


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, key_binder):
        self.keybinder = key_binder
        super().__init__()

    def nativeEventFilter(self, event_type, message):
        ret = self.keybinder.handler(event_type, message)
        return ret, 0


def run():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    settings = QSettings("MySoft", "DropdownMenu")
    # settings.clear()
    if settings.value("Initial/is_initiated") != "true":
        print("INITIAL START")
        InitialConfig.initiation(app)

    app.drop_menu_window = DropMenu.DropMenu(app)
    app.tray = Tray.Tray(
                        app,
                        click_funk=app.drop_menu_window.show_hide,
                        show_hide_funk=app.drop_menu_window.show_hide,
                        settings_funk=Settings.start_settings_constr(app, app.drop_menu_window)
                        )
    # window.show()

    keybinder.init()

    keybinder.register_hotkey(app.drop_menu_window.winId(), "Shift+Ctrl+A", app.drop_menu_window.show_hide)

    win_event_filter = WinEventFilter(keybinder)
    event_dispatcher = QAbstractEventDispatcher.instance()
    event_dispatcher.installNativeEventFilter(win_event_filter)

    app.setQuitOnLastWindowClosed(False)
    app.exec_()

    keybinder.unregister_hotkey(app.drop_menu_window.winId(), "Shift+Ctrl+A")


if __name__ == '__main__':
    sys.exit(run())
