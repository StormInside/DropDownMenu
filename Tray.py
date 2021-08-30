from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, \
    QSystemTrayIcon, \
    QAction, \
    qApp, \
    QMenu


class Tray(QSystemTrayIcon):
    def __init__(self, app: QApplication, click_funk, show_hide_funk, settings_funk):
        self.click_funk = click_funk
        super().__init__()
        self.setIcon(QIcon("Icons/DropDownLogo_gray.png"))  # TODO Create icon

        show_hide_action = QAction("Show / Hide", self)
        settings_action = QAction("Settings", self)
        quit_action = QAction("Exit", self)

        show_hide_action.triggered.connect(show_hide_funk)
        settings_action.triggered.connect(settings_funk)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_hide_action)
        tray_menu.addAction(settings_action)
        tray_menu.addAction(quit_action)

        self.activated.connect(self.tray_click_constr())
        self.setContextMenu(tray_menu)
        self.show()

    def tray_click_constr(self):
        def tray_click(reason):
            if reason == QSystemTrayIcon.Trigger:
                self.click_funk()

        return tray_click
