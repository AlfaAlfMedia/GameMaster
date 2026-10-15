"""Tests for gamemaster.configfile.

Run from the root of the repository:

    PYTHONPATH=usr/lib/python3/dist-packages python3 -m unittest discover tests
"""

import unittest

from gamemaster import configfile


class ReadValuesTest(unittest.TestCase):
    def test_pair_of_quotes_is_dropped(self) -> None:
        values = configfile.read_values('A="x y"\nB=\'z\'\nC=plain\n')
        self.assertEqual(values, {"A": "x y", "B": "z", "C": "plain"})

    def test_quotes_that_belong_to_the_value_stay(self) -> None:
        values = configfile.read_values('NAME=GM Test "Nord"\nP=ab"\nQ="\n')
        self.assertEqual(values["NAME"], 'GM Test "Nord"')
        self.assertEqual(values["P"], 'ab"')
        self.assertEqual(values["Q"], '"')

    def test_reference_to_an_earlier_setting(self) -> None:
        values = configfile.read_values("PORT=2456\nHOOK=/bin/echo $PORT ${PORT}\n")
        self.assertEqual(values["HOOK"], "/bin/echo 2456 2456")


if __name__ == "__main__":
    unittest.main()
