import unittest
from .context import lyrical
from lyrical.model import Database, Song

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.a = Song(None, 'Amazing Grace', """Amazing Grace, how sweet the sound,
                                  That saved a wretch like me
                                  I once was lost but now am found,
                                  Was blind but now I see.

                                  'Twas Grace that taught
                                  my heart to fear
                                  And Grace, my fears relieved
                                  How precious did that Grace appear
                                  the hour I first believed""", None)
        self.b = Song(None, 'Grace Like Rain', """Amazing grace, how sweet the sound
                                    That saved a wretch like me
                                    I once was lost, but now I'm found
                                    Was blind, but now I see so clearly

                                    Hallelujah
                                    Grace Like Rain falls down on me
                                    And hallelujah
                                    And all my stains are washed away
                                    They're washed away""", '2003 Todd Aglow')

    def db(self):
        db = Database(':memory:')
        db.create_tables()
        return db

    def test_adding_song(self):
        db = self.db()
        self.assertEqual(db.add_song(self.a), 1)

    def test_finding_songs(self):
        db = self.db()
        db.add_song(self.a, self.b)
        results = db.find_songs('grace')
        self.assertEqual(len(results), 2)
        titles = [song.title for song in results]
        self.assertTrue(self.a.title in titles)
        self.assertTrue(self.b.title in titles)

    def test_fetching_song(self):
        pass

    def test_removing_song(self):
        pass

    def test_updating_song(self):
        db = self.db()
        song = Song(None, 'test a', 'foobar')
        id = db.push_song(song)
        song.id = id
        song.title = 'test b'
        db.push_song(song)
        result = db.find_songs('foobar')
        self.assertEqual(result[0].title, 'test b')
