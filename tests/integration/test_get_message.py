import unittest

from api import app


class GetMessageTest(unittest.TestCase):

    def setUp(self):
        self.app = app

    def test_something(self):
        expected = {'my-message': 'w00t_1'}

        with self.app.test_client() as client:
            actual = client.get('/message/1')

        self.assertEqual(expected, actual.get_json())
