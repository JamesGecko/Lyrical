from gui.ui_editor import Ui_Editor
from model import Song
from PySide import QtCore
from PySide.QtGui import QMainWindow

class LyricalEditor(QMainWindow, Ui_Editor):
    def __init__(self, db, callbacks=None, song=None):
        '''Takes a database object, an (optional) list of functions to
        execute on save, and an (optional) Song.
        '''
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.db = db
        self.callbacks = callbacks if callbacks else []
        self.song = song if song else Song(None, '', '', '')
        self.changes_since_save = False

        self.save_button.clicked.connect(self.save_song)

        self.title.setText(self.song.title)
        self.lyrics.setPlainText(self.song.lyrics)

    @QtCore.Slot()
    def close_window(self):
        # TODO: check if changes have been made since save.
        if self.title != self.song.title or self.lyrics != self.song.lyrics:
            pass
        self.close()

    @QtCore.Slot()
    def save_song(self):
        self.song.title = self.title.text()
        self.song.lyrics = self.lyrics.toPlainText()

        if self.song.validate()[0]:
            self.db.push_song(self.song)
            for callback in self.callbacks:
                apply(callback)
            self.close_window()
        else:
            print "Validation failed!"
            print self.song.validate()[1]
            # TODO: show error dialog


