import sys
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher, Qt, QSettings
from PyQt5.QtWidgets import QApplication

from pyqtkeybind import keybinder
# import keyboard
import HotkeyManager

import DropMenu
import SettingsW
import Tray
import InitialConfig





def run():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)

    app.setOrganizationName("MySoft")
    app.setOrganizationDomain("mysoft.com")
    app.setApplicationName("DropdownMenu")  # TODO org name

    app.hotkey_manager = HotkeyManager.HotkeyManager(app)

    settings = QSettings()
    settings.clear()
    if settings.value("Initial/is_initiated") != "true":
        print("INITIAL START")
        InitialConfig.initiation(app)

    print("in appstart_________________")
    for key in settings.allKeys():
        print(f"{key} == {settings.value(key)}")

    app.drop_menu_window = DropMenu.DropMenu(app)
    app.tray = Tray.Tray(
                        app,
                        click_funk=app.drop_menu_window.show_hide,
                        show_hide_funk=app.drop_menu_window.show_hide,
                        settings_funk=SettingsW.start_settings_constr(app, app.drop_menu_window)
                        )
    # window.show()

    open_hotkey = settings.value("Hotkey/open_hotkey")
    print(open_hotkey)

    # keyboard.add_hotkey("Shift+Ctrl+A", app.drop_menu_window.show_hide)
    # keybinder.init()
    #
    # keybinder.register_hotkey(app.drop_menu_window.winId(), "Shift+Ctrl+A", app.drop_menu_window.show_hide)
    #
    # win_event_filter = WinEventFilter(keybinder)
    # event_dispatcher = QAbstractEventDispatcher.instance()
    # event_dispatcher.installNativeEventFilter(win_event_filter)

    app.setQuitOnLastWindowClosed(False)
    app.exec_()

    # keybinder.unregister_hotkey(app.drop_menu_window.winId(), "Shift+Ctrl+A")



if __name__ == '__main__':
    sys.exit(run())
