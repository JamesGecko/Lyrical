import sys
from PySide.QtGui import QApplication, QMainWindow, QWidget
from PySide.QtGui import QDesktopWidget
from PySide.QtCore import *
from gui.ui_mainwindow import Ui_MainWindow
from gui.ui_projector import Ui_Projector
import model
from sys import stderr

class Slide(object):
    def __init__(self, title, content):
        self.title = title
        self.content = content

class LyricalProjector(QWidget, Ui_Projector):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

class LyricalControl(QMainWindow, Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

    @Slot()
    def foo(self):
        windows[1].show()
        windows[0].hide()

    def update(slide):
        '''set title and content to slide
        '''
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = []
    windows.append(LyricalControl())
    windows.append(LyricalProjector())
    windows[0].show()
    #windows[1].showFullScreen()
    #windows[1].show()

    desktop = QDesktopWidget()
    if desktop.screenCount() < 2:
        stderr.write('Need at least two screens connected.')
        sys.exit()
    else:
        sys.exit(app.exec_())
