import unittest

import sqreened_app


class Sqreened_appTestCase(unittest.TestCase):

    def setUp(self):
        self.app = sqreened_app.app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertIn('Welcome to sqreened-app', rv.data.decode())


if __name__ == '__main__':
    unittest.main()
