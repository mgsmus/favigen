import unittest
import os

from favigen import Favigen


class FavigenTestCase(unittest.TestCase):

    def test_dirs(self):
        favigen = Favigen()
        favigen.make_dirs()
        self.assertTrue(os.path.exists(favigen.tmp_path and favigen.output_path))


