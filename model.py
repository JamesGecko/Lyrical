import sqlite3

class Song(object):
    def __init__(self, id=None, title=None, lyrics=None, copyright=None):
        self.title = title
        self.lyrics = lyrics
        self.copyright = copyright
        self.id = id

    def lyrics_list(self):
        return self.lyrics.split('\n\n')

    def validate(self):
        if self.title == '':
            return 'Title cannot be blank'
        if self.lyrics == '':
            return 'Lyrics cannot be empty'

class Database(object):
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.c = self.conn.cursor()

    def create_tables(self):
        self.c.execute('CREATE TABLE songs ( '
                       'id INTEGER PRIMARY KEY, '
                       'title STRING, '
                       'lyrics STRING, '
                       'copyright STRING)')

    def add_song(self, *songs):
        rowids = []
        for song in songs:
            self.c.execute('INSERT INTO songs (title, lyrics, copyright) '
                            'VALUES (?, ?, ?)',
                            (song.title, song.lyrics, song.copyright))
            rowids.append(self.c.lastrowid)
        self.conn.commit()
        if len(rowids) == 1:
            return rowids[0]
        else:
            return rowids

    def update_song(self, song):
        try:
            self.c.execute('UPDATE songs SET title=?, lyrics=?, copyright=? '
                           'WHERE id=?',
                           (song.title, song.lyrics, song.copyright, song.id))
            self.conn.commit()
            return True
        except:
            return False

    def push_song(self, song):
        if song.id:
            self.update_song(song)
        else:
            self.add_song(song)

    def find_songs(self, query=None):
        '''Returns a list of Song objects containing the query string.
        If the query is empty, return all of them.
        '''
        if query:
            query = "%%%s%%" % query
            self.c.execute("SELECT DISTINCT id, title, lyrics, copyright "
                           "FROM songs WHERE title LIKE ? OR lyrics LIKE ?",
                           (query, query))
        else:
            self.c.execute("SELECT id, title, lyrics, copyright FROM songs")
        results = self.c.fetchall()
        return [Song(r[0], r[1], r[2], r[3]) for r in results]

    def get_song(self, id):
        self.c.execute("SELECT TOP 1 title, lyrics, copyright"
                       "FROM songs where id = ?", (id,))
        return Song(*self.c.fetchone())

    def __del__(self):
        self.c.close()
