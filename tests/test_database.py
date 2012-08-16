import unittest
from model import Database, Song

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.a = Song('Amazing Grace', """Amazing Grace, how sweet the sound,
                                  That saved a wretch like me
                                  I once was lost but now am found,
                                  Was blind but now I see.

                                  'Twas Grace that taught
                                  my heart to fear
                                  And Grace, my fears relieved
                                  How precious did that Grace appear
                                  the hour I first believed""", None)
        self.b = Song('Grace Like Rain', """Amazing grace, how sweet the sound
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
        result = db.find_songs('grace')
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].title, self.a.title)
        self.assertEqual(result[1].title, self.b.title)

    def test_getting_title_list(self):
        db = self.db()
        db.add_song(self.a, self.b)
        results = db.find_songs('grace')
        for song in results:
            print song.title
        titles = [song.title for song in results]
        self.assertEqual(results[0].title, 'Amazing Grace')
        self.assertEqual(results[1].title, 'Grace Like Rain')


if __name__ == '__main__':
    unittest.main()
