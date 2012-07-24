import sqlite3

class Song(object):
    def __init__(self, title=None, lyrics=None, copyright=None):
        self.lyrics = """Amazing Grace, how sweet the sound,
That saved a wretch like me
I once was lost but now am found,
Was blind but now I see.

'Twas Grace that taught
my heart to fear
And Grace, my fears relieved
How precious did that Grace appear
the hour I first believed

Through many dangers, toils and snares
we have already come
'Twas Grace that brought us safe thus far
and Grace will lead us home

The Lord has promised good to me
His word my hope secures
He will my shield and portion be
as long as life endures

When we've been here ten thousand years
bright shining as the sun
We've no less days to sing God's praise
then when we've first begun

Amazing Grace, how sweet the sound
That saved a wretch like me
I once was lost but now am found
Was blind but now I see"""

        self.title = 'Amazing Grace'
        self.copyright = ''

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

    def generate_new(self):
        self.c.execute('CREATE TABLE songs ( '
                       'id INTEGER PRIMARY KEY, '
                       'title STRING, '
                       'lyrics STRING, '
                       'copyright STRING)')

    def add_song(self, song):
        try:
            self.c.execute('INSERT INTO songs (title, lyrics, copyright) '
                           'VALUES (?, ?, ?)',
                           (song.title, song.lyrics, song.copyright))
            self.c.commit()
            return self.c.lastrowid
        except:
            return False

    def update_song(self, song):
        try:
            self.c.execute('UPDATE songs SET title=?, lyrics=?, copyright=? '
                           'WHERE id=?',
                           (song.title, song.lyrics, song.copyright, song.id))
            self.c.commit()
            return True
        except:
            return False

    def push_song(self, song):
        if song.id:
            update_song(song)
        else:
            add_song(song)

    def find_song(self, query):
        self.c.execute("SELECT * FROM song WHERE title LIKE '?' "
                       "OR lyrics LIKE '?'", query)
        return self.c.fetchall()

    def find_all_songs(self):
        self.c.execute("SELECT * FROM song")
        return self.c.fetchall()

    def get_song(self, id):
        self.c.execute("SELECT TOP 1 * FROM song where id = ?", id)
        return Song(

    def __del__(self):
        self.c.close()
