import sys
import os, errno
from PySide.QtGui import QApplication, QMainWindow, QWidget
from PySide.QtGui import QDesktopWidget
from PySide import QtCore
from gui.ui_mainwindow import Ui_MainWindow
from gui.ui_projector import Ui_Projector
from model import Database, Song
from sys import stderr

class Slide(object):
    def __init__(self, title, content):
        self.title = title
        self.content = content

class LyricalProjector(QWidget, Ui_Projector):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)

    def update(self, slide):
        '''set title and content to slide
        '''
        self.title.setText(slide.title)
        self.content.setText(slide.content)

class LyricalControl(QMainWindow, Ui_MainWindow):
    def __init__(self, projector_window):
        QMainWindow.__init__(self)
        self.projector = projector_window
        self.setupUi(self)

        self.lyrics.clicked.connect(self.update_screen)

    @QtCore.Slot()
    def update_screen(self):
        title = self.song_list.currentItem().text()
        content = self.lyrics.currentItem().text()
        self.projector.update(Slide(title, content))


def get_database():
    data_directory = os.path.expanduser('~/.lyrical')
    try:
        os.makedirs(data_directory)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    db = Database(data_directory + '/songs.sqlite')
    return db


if __name__ == '__main__':
    app = QApplication(sys.argv)
    projector = LyricalProjector()
    controller = LyricalControl(projector)
    controller.show()
    projector.show()

    db = get_database()

    song = Song()
    controller.lyrics.insertItems(0, song.lyrics_list())
    controller.lyrics.setCurrentRow(0)
    controller.song_list.addItem(song.title)
    controller.song_list.setCurrentRow(0)

    desktop = QDesktopWidget()
    if desktop.screenCount() < 2:
        stderr.write('Need at least two screens connected.')
        sys.exit()
    else:
        sys.exit(app.exec_())
