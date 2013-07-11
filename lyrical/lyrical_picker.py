from gui.ui_picker import Ui_Picker
from PySide import QtCore
from PySide.QtGui import QMainWindow
from lyrical_editor import LyricalEditor

class LyricalPicker(QMainWindow, Ui_Picker):
    def __init__(self, db, controller):
        QMainWindow.__init__(self)
        self.db = db
        self.songs = []
        self.controller = controller
        self.editors = []
        self.setupUi(self)

        self.song_list.clicked.connect(self.click_song)
        self.song_list.doubleClicked.connect(self.add_song)
        self.add_button.clicked.connect(self.add_song)
        self.edit_button.clicked.connect(self.edit_song)
        self.new_button.clicked.connect(self.edit_song)
        self.cancel_button.clicked.connect(self.close_window)
        self.search_text.textChanged.connect(self.search)

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Escape:
            self.close()

    def show_lyrics(self, lyrics):
        '''Update the lyrics QListWidget
        '''
        self.lyrics.clear()
        self.lyrics.insertItems(0, lyrics)
        self.lyrics.setCurrentRow(0)

    def selected_song(self):
        '''Get the Song for the currently selected title.
        '''
        song_index = self.song_list.currentRow()
        if self.songs:
            return self.songs[song_index]

    @QtCore.Slot()
    def click_song(self):
        '''When clicked, show correct lyrics.
        '''
        if self.song_list.count() > 0 and any(self.songs):
            i = self.song_list.currentRow()
            self.show_lyrics(self.songs[i].lyrics_list())

    @QtCore.Slot()
    def add_song(self):
        '''Give LyricalControl the song
        '''
        self.controller.add_song(self.selected_song())

    @QtCore.Slot()
    def edit_song(self):
        '''Give a LyricalEditor instance the song
        '''
        editor = LyricalEditor(self.db, (self.click_song,),
                               self.selected_song())
        editor.show()
        self.editors.append(editor)

    @QtCore.Slot()
    def search(self):
        self.songs = self.db.find_songs(self.search_text.text())

        titles = [song.title for song in self.songs]
        self.song_list.clear()
        self.song_list.insertItems(0, titles)
        self.song_list.setCurrentRow(0)

        if any(self.songs):
            self.show_lyrics(self.songs[0].lyrics_list())

    @QtCore.Slot()
    def close_window(self):
        self.close()


