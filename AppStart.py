import sys
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher, Qt
from PyQt5.QtWidgets import QApplication

from pyqtkeybind import keybinder

import DropMenu
import Settings
import Tray
import Resize_try


class WinEventFilter(QAbstractNativeEventFilter):
    def __init__(self, key_binder):
        self.keybinder = key_binder
        super().__init__()

    def nativeEventFilter(self, event_type, message):
        ret = self.keybinder.handler(event_type, message)
        return ret, 0


def initial_configure_size(app, w_mul, h_mul, settings_w_mul, settings_h_mul):
    screen = app.primaryScreen()

    size = screen.size()

    main_window_w = size.width() * w_mul
    main_window_h = size.height() * h_mul

    main_window_off_w = (size.width() - main_window_w) // 2

    settings_window_w = size.width() * settings_w_mul
    settings_window_h = size.height() * settings_h_mul

    size = {"main_window_w": main_window_w,
            "main_window_h": main_window_h,
            "main_window_off_w": main_window_off_w,
            "settings_window_w": settings_window_w,
            "settings_window_h": settings_window_h}

    return size


def run():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    size = initial_configure_size(app, 0.9, 0.6, 0.2, 0.5)
    app.drop_menu_window = DropMenu.DropMenu(app,
                                         width=size["main_window_w"],
                                         height=size["main_window_h"],
                                         x=size["main_window_off_w"]
                                         )
    app.tray = Tray.Tray(app,
                     click_funk=app.drop_menu_window.show_hide,
                     show_hide_funk=app.drop_menu_window.show_hide,
                     settings_funk=Settings.start_settings_constr(app, size, app.drop_menu_window)
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
