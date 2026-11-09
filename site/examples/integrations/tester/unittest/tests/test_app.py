import Pyjo.Test
import Pyjo.Test.Pyjo

from Pyjo.File import curfile

import unittest


# The assertions raise AssertionError instead of printing TAP, as unittest takes them
def setUpModule():
    Pyjo.Test.raise_failures()


def tearDownModule():
    Pyjo.Test.raise_failures(False)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.t = Pyjo.Test.Pyjo.new(curfile().dirname().sibling('app.py'))
        self.addCleanup(self.t.close)

    def test_hello(self):
        self.t.get_ok('/hello/Sara').status_is(200).json_is('/hello', 'Sara')

    def test_items(self):
        self.t.post_ok('/items', json={'name': 'Pen'}).status_is(201).json_is('/name', 'Pen')
        self.t.post_ok('/items', json={}).status_is(400)
        self.assertEqual(self.t.tx.res.json('/error'), 'name required')


if __name__ == '__main__':
    unittest.main()
