import os
import run
import unittest
import tempfile
import sys
class FlaskrTestCase(unittest.TestCase):
    def setUp(self):
        self.app = run.app.test_client()
        print sys.argv
        #self.arg = '2'
    def test_method(self):
        rv = self.app.get('/legal', data = dict(key='D439EDD7A795FF0199ABBB1ADCC23194D521E783B1A14609F9A0220C1C20AE03'), follow_redirects=True)
        #print rv
        print rv.data
        #assert 'No entries here so far' not in rv.data
        #assert '&lt;Hello&gt;' in rv.data
        #assert '<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
        unittest.main()
