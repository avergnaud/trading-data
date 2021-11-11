# -*- coding: utf-8 -*-

import unittest
from sample.helpers import Helpers


class HelpersTestCase(unittest.TestCase):
    """Basic test cases."""

    def test_add(self):
        helpers = Helpers()
        self.assertEqual(helpers.add(2, 3), 5)
