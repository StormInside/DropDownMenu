import sys
from PyQt5.QtCore import QAbstractNativeEventFilter, QAbstractEventDispatcher, Qt
from PyQt5.QtWidgets import QApplication

import AllWindows


def run():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)

    app = QApplication(sys.argv)
    window = AllWindows.Main(app)
    # window.show()


    app.setQuitOnLastWindowClosed(False)
    app.exec_()



if __name__ == '__main__':

    sys.exit(run())



