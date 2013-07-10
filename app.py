import sys
import os, errno
from PySide.QtGui import QApplication, QMainWindow, QWidget
from PySide.QtGui import QDesktopWidget
from PySide import QtCore
from gui.ui_mainwindow import Ui_MainWindow
from gui.ui_projector import Ui_Projector
from gui.ui_editor import Ui_Editor
from gui.ui_picker import Ui_Picker
from model import Database, Song
from sys import stderr

class Slide(object):
    def __init__(self, title, content):
        self.title = title
        self.content = self.convert_line_breaks(content)

    def convert_line_breaks(self, text):
        return text.replace('\n', '<br>')


class LyricalProjector(QWidget, Ui_Projector):
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.style = '''
        color: white;
        background-color: black;
        padding-top: 20px;
        padding-left: 20px;
        font-size: 40px;
        text-align: center;
        ''' #TODO: text-align doesn't work with QTextBrowser widgets
        self.content.setStyleSheet(self.style)

    def update(self, slide):
        '''set title and content to slide
        '''
        self.title.setText(slide.title)
        self.content.setText(slide.content)

    def focusInEvent(self):
        '''When focused, set the focus back to the control window.
        '''
        pass

class LyricalControl(QMainWindow, Ui_MainWindow):
    def __init__(self, projector_window):
        QMainWindow.__init__(self)
        self.projector = projector_window
        self.setupUi(self)
        self.songs = []

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
        db = get_database() #TODO: is multiple sqlite db handles the best way?
        self.picker = LyricalPicker(db, self)
        self.picker.show()


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


def get_database():
    data_directory = os.path.expanduser('~/.lyrical')
    try:
        os.makedirs(data_directory)
        db = Database(data_directory + '/songs.sqlite')
        db.create_tables()
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise
    db = Database(data_directory + '/songs.sqlite')
    return db

def main():
    app = QApplication(sys.argv)
    projector = LyricalProjector()
    controller = LyricalControl(projector)
    projector.show()
    controller.show()

    #db = get_database()
    #editor = LyricalEditor(db)
    #editor.show()

    song = Song(None, 'Amazing Grace', """Amazing Grace, how sweet the sound,
That saved a wretch like me
I once was lost but now am found,
Was blind but now I see.

'Twas Grace that taught
my heart to fear
And Grace, my fears relieved
How precious did that Grace appear
the hour I first believed""")
    controller.add_song(song)

    desktop = QDesktopWidget()
    if desktop.screenCount() < 2:
        stderr.write('Need at least two screens connected.')
        sys.exit()
    else:
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
