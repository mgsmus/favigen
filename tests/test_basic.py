"""Unit tests"""

import sys
import unittest
import os
from favigen import Favigen


class FavigenTestCase(unittest.TestCase):
    """Basic test case"""

    def test_dirs(self):
        """Test directories"""
        favigen = Favigen()
        favigen.make_dirs()
        self.assertTrue(os.path.exists(favigen.tmp_path and favigen.output_path))

    def test_argparser(self):
        """Test argument parser"""
        favigen = Favigen()
        arg_name = 'logo.png'
        sys.argv[1:] = [arg_name]
        self.assertEqual(arg_name, favigen.parser.parse_args().file)

    def test_extras(self):
        """Test extras"""
        favigen = Favigen()
        favigen.make_dirs()
        favigen.create_extras()
        browserconfig_xml = os.path.join(favigen.tmp_path, 'browserconfig.xml')
        manifest_json = os.path.join(favigen.tmp_path, 'manifest.json')
        html_txt = os.path.join(favigen.tmp_path, 'html.txt')
        self.assertTrue(
            os.path.exists(browserconfig_xml)
            and os.path.exists(manifest_json)
            and os.path.exists(html_txt)
        )
