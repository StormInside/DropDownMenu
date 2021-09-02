from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QWidget
from PyQt5.QtCore import QSettings

from auto_generated_UI import UI_settings


def center(window):
    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())


def start_settings_constr(app, window_to_hide):
    def start_settings(self):
        app.settings = SettingsW(app)
        app.settings.show()
        window_to_hide.hide()

    return start_settings


class SettingsW(QMainWindow, UI_settings.Ui_Settings):
    def __init__(self, app):
        super().__init__()
        self.setupUi(self)

        self.app = app
        self.wind_active_on_prev_check = False

        settings = QSettings()
        settings.beginGroup("Screen")
        self.resize(settings.value("sett_frame_geometry"))
        if settings.value("sett_pos") == "Center":
            center(self)
        else:
            self.move(settings.value("sett_pos"))
        settings.endGroup()
        self.settings = settings

        self.setWindowTitle("Settings")
        self.setStyleSheet("QMainWindow{background-color: black;border: 1px solid white}")

        self.hotkey_input.keySequenceChanged.connect(self._change_key_sequence)
        self.hotkey_input.setKeySequence(self.settings.value("Hotkey/open_hotkey"))
        # self.setWindowFlags()

        self.app.focusChanged.connect(self.on_focus_change)

    def on_focus_change(self, old_widget: QWidget, new_widget: QWidget):

        # old_widget_name = old_widget.objectName() if not (old_widget is None) else "None"
        # new_widget_name = new_widget.objectName() if not (new_widget is None) else "None"
        # print(f"old_widget:{old_widget_name} - new_widget: {new_widget_name}")
        print(f"wind_active_on_prev_check:{self.wind_active_on_prev_check} - isActiveWindow: {self.isActiveWindow()}")
        if self.wind_active_on_prev_check and (not self.isActiveWindow()):
            self.enable_open_hotkey() #TODO fix slow closing of window, caused by long execution time of this line
        elif (not self.wind_active_on_prev_check) and self.isActiveWindow():
            self.disable_open_hotkey()
        self.wind_active_on_prev_check = self.isActiveWindow()


    def disable_open_hotkey(self):
        old_hotkey = self.settings.value("Hotkey/open_hotkey")
        self.app.keybinder.unregister_hotkey(self.app.drop_menu_window.winId(), old_hotkey)

    def enable_open_hotkey(self):
        new_hotkey = self.settings.value("Hotkey/open_hotkey")
        self.app.keybinder.register_hotkey(self.app.drop_menu_window.winId(),
                                           new_hotkey,
                                           self.app.drop_menu_window.show_hide)

    def _change_key_sequence(self, key_seq: QKeySequence):
        print(key_seq.toString())
        mod_key_seq = QKeySequence((key_seq.toString()).split(',')[0].strip())
        self.hotkey_input.setKeySequence(mod_key_seq)
        self.settings.setValue("Hotkey/open_hotkey", mod_key_seq)