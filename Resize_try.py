from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, \
                            QMainWindow, \
                            QSystemTrayIcon, \
                            QAction, \
                            qApp, \
                            QMenu, \
                            QDesktopWidget,\
                            QSizeGrip, QWidget

from auto_generated_UI import settigsUi

def center(window):
    qtRectangle = window.frameGeometry()
    centerPoint = QDesktopWidget().availableGeometry().center()
    qtRectangle.moveCenter(centerPoint)
    window.move(qtRectangle.topLeft())


class Main(QMainWindow):
    _gripSize = 8
    def __init__(self, app: QApplication,
                 width=1800,
                 height=600,
                 x=60,
                 y=0,
                 settings_width=1280,
                 settings_height=720):
        super().__init__()

        self.settings_width = settings_width
        self.settings_height = settings_height

        self.setFixedSize(width, height)
        self.move(x, y)
        self.setStyleSheet("QMainWindow{background-color: darkgray;border: 1px solid black}")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)

        self.setFocusPolicy(Qt.NoFocus)

        app.focusChanged.connect(self.on_focus_change)

        self.configure_tray()

        self.sideGrips = [
            SideGrip(self, Qt.LeftEdge),
            SideGrip(self, Qt.TopEdge),
            SideGrip(self, Qt.RightEdge),
            SideGrip(self, Qt.BottomEdge),
        ]


    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        # an "inner" rect used for reference to set the geometries of size grips
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)


        # left edge
        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())
        # top edge
        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)
        # right edge
        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())
        # bottom edge
        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QMainWindow.resizeEvent(self, event)
        self.updateGrips()

    def on_focus_change(self):
        # print(self.hasFocus())
        if not self.isActiveWindow():
            self.hide()

    def show_hide(self):
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.setFocus()
            self.activateWindow()


    def start_settings(self):
        self.settings = Settings()
        self.hide()
        self.settings.show()


    def tray_click(self, reason):
        if reason == QSystemTrayIcon.Trigger:
            self.show_hide()

    def configure_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon("DropDownLogo_gray.png"))  # TODO Create icon

        show_hide_action = QAction("Show / Hide", self)
        settings_action = QAction("Settings", self)
        quit_action = QAction("Exit", self)

        show_hide_action.triggered.connect(self.show_hide)
        settings_action.triggered.connect(self.start_settings)
        quit_action.triggered.connect(qApp.quit)

        tray_menu = QMenu()
        tray_menu.addAction(show_hide_action)
        tray_menu.addAction(settings_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.activated.connect(self.tray_click)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

class SideGrip(QWidget):
    def __init__(self, parent, edge):
        QWidget.__init__(self, parent)
        if edge == Qt.LeftEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == Qt.TopEdge:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == Qt.RightEdge:
            self.setCursor(Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None

class Settings(QMainWindow, settigsUi.Ui_Settings):
    def __init__(self, width=1280, height=720, x=0.5, y=0):
        super().__init__()

        self.setupUi(self)

        self.setFixedSize(width, height)
        if isinstance(x, float):
            center(self)
        else:
            self.move(x, y)

        self.setWindowTitle("Settings")
        self.setStyleSheet("QMainWindow{background-color: black;border: 1px solid white}")
        # self.setWindowFlags()

    # def closeEvent(self, event):

