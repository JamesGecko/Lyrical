from gui.ui_mainwindow import Ui_MainWindow
from PySide.QtGui import QApplication, QMainWindow
from PySide import QtCore
from lyrical_picker import LyricalPicker
from slide import Slide

class LyricalControl(QMainWindow, Ui_MainWindow):
    def __init__(self, projector_window, db):
        QMainWindow.__init__(self)
        self.projector = projector_window
        self.setupUi(self)
        self.songs = []
        self.db = db

        self.song_list.clicked.connect(self.click_song)
        self.lyrics.clicked.connect(self.update_screen)
        self.add_button.clicked.connect(self.show_picker)

    def add_song(self, song):
        self.songs.append(song)
        self.song_list.addItem(song.title)

    def remove_song(self):
        #controller.song_list.removeCurrentRow(0)
        pass

    def edit_song(self):
        #controller.song_list.getCurrentRow()
        pass

    def show_lyrics_list(self, lyrics):
        self.lyrics.clear()
        self.lyrics.insertItems(0, lyrics)
        self.lyrics.setCurrentRow(0)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            sys.exit()

    @QtCore.Slot()
    def click_song(self):
        '''When clicked, show correct lyrics
        '''
        if self.song_list.count() > 0 and any(self.songs):
            i = self.song_list.currentRow()
            self.show_lyrics_list(self.songs[i].lyrics_list())

    @QtCore.Slot()
    def update_screen(self):
        title = self.song_list.currentItem().text()
        content = self.lyrics.currentItem().text()
        self.projector.update(Slide(title, content))

    @QtCore.Slot()
    def show_picker(self):
        self.picker = LyricalPicker(self.db, self)
        self.picker.show()

