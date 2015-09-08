#!/usr/bin/env python
import sys
import os, errno
from PySide.QtGui import QApplication
from PySide.QtGui import QDesktopWidget
from PySide.QtGui import QMessageBox
from PySide.QtGui import QWidget
from model import Database, Song
from sys import stderr

from lyrical_projector import LyricalProjector
from lyrical_control import LyricalControl

def get_database():
    #TODO: is multiple sqlite db handles the best way?
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

class ModalDialog(QWidget):
    def error(self, message):
        QMessageBox.critical(self, "Error", message)

def main():
    db = get_database()
    app = QApplication(sys.argv)
    projector = LyricalProjector()
    controller = LyricalControl(projector, db)
    projector.show()
    controller.show()
    controller.raise_()

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
        error = ModalDialog()
        error.error('Need at least two screens connected.')
        sys.exit()
    else:
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()
