import unittest
from random import randint

from api import append_id


class AppendIdTest(unittest.TestCase):

    def test_append_id_message(self):
        message_id = randint(1, 100)

        expected = f'w00t_{message_id}'
        actual = append_id(message_id)

        self.assertEqual(expected, actual)
