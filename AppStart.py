import sys
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher
from PyQt5.QtWidgets import QApplication
import keyboard

import AllWindows


def run():
    app = QApplication(sys.argv)
    window = AllWindows.Main(app)
    # window.show()

    keyboard.add_hotkey('ctrl+shift+a', window.show_hide, suppress=True)

    app.setQuitOnLastWindowClosed(False)
    app.exec_()



if __name__ == '__main__':

    sys.exit(run())



