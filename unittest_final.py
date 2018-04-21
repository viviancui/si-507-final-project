import unittest
import data_database
import model
import sqlite3
import data_spotify
import musixmatch_request

DBNAME = 'whatdidtheysay.db'
class TestDatabase(unittest.TestCase):
    def test_Artists_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT Artist_name FROM Artists'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Megadeth',), result_list)
        self.assertIn(('Slayer',), result_list)
        conn.close()

    def test_Albums_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT DISTINCT Album_name
            FROM Albums JOIN Artists
            ON Albums.Artist_id = Artists.Artist_id
            WHERE Albums.Release_date="1990" and Artists.Artist_name="Megadeth"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Rust In Peace',), result_list)
        self.assertIn(('Killing Is My Business… and Business Is Good!',), result_list)
        self.assertEqual(len(result_list), 3)

    def test_tracks_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Track_name
            FROM Tracks JOIN Artists
            ON Tracks.Artist_id = Artists.Artist_id
            WHERE Artists.Artist_name="Megadeth"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Hangar 18',), result_list)
        self.assertIn(('Five Magics',), result_list)
        self.assertIn(('Lucretia',), result_list)
        conn.close()

class TestModel(unittest.TestCase):

    def test_release_year(self):
        results = model.releaseYear('Megadeth')
        self.assertEqual(results[1][0], 2)

    def test_track_length(self):
        results = model.trackLength('Megadeth')
        self.assertEqual(results[1][0], 236.0)

    def test_release_year(self):
        results = model.releaseYear('Slayer')
        self.assertEqual(results[1][0], 3)

    def test_track_length(self):
        results = model.trackLength('Metallica')
        self.assertEqual(results[1][0], 313.25)

class TestRequest(unittest.TestCase):

    def test_get_artist_obj(self):
        results = musixmatch_request.get_artist_obj('Megadeth')
        self.assertEqual(results.artist_name, 'Megadeth')
        self.assertEqual(results.artist_id, '521')

    def test_get_artist_obj(self):
        results = musixmatch_request.get_artist_obj('Slayer')
        self.assertEqual(results.artist_name, 'Slayer')
        self.assertEqual(results.artist_id, 2683)

unittest.main()
