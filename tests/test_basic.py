import sys
import unittest
import os

from favigen import Favigen


class FavigenTestCase(unittest.TestCase):

    def test_dirs(self):
        favigen = Favigen()
        favigen.make_dirs()
        self.assertTrue(os.path.exists(favigen.tmp_path and favigen.output_path))

    def test_argparser(self):
        favigen = Favigen()
        arg_name = 'logo.png'
        sys.argv[1:] = [arg_name]
        self.assertEqual(arg_name, favigen.parser.parse_args().file)

    def test_extras(self):
        favigen = Favigen()
        favigen.make_dirs()
        favigen.create_extras()
        b = os.path.join(favigen.tmp_path, 'browserconfig.xml')
        m = os.path.join(favigen.tmp_path, 'manifest.json')
        h = os.path.join(favigen.tmp_path, 'html.txt')
        self.assertTrue(os.path.exists(b and m and h))
