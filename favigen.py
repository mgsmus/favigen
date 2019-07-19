#!/usr/bin/env python

"""
Favigen is a very simple Python application for creating common favicon and app icons.
"""

import argparse
import sys
import os
import math
import datetime
from shutil import make_archive, rmtree
from pathlib import Path
from PIL import Image
import extras


class Favigen:
    """Favigen, favicon and app icon maker"""

    def __init__(self):
        self.base_path = Path(__file__).resolve().parent
        self.tmp_dir = "tmp"
        self.output_dir = "output"
        self.tmp_path = os.path.join(self.base_path, self.tmp_dir)
        self.output_path = os.path.join(self.base_path, self.output_dir)
        self.icons = {
            "android-icon-144x144.png":   [144, 144],
            "android-icon-192x192.png":   [192, 192],
            "android-icon-36x36.png":     [36, 36],
            "android-icon-48x48.png":     [48, 48],
            "android-icon-72x72.png":     [72, 72],
            "android-icon-96x96.png":     [96, 96],
            "apple-icon.png":             [192, 192],
            "apple-icon-114x114.png":     [114, 114],
            "apple-icon-120x120.png":     [120, 120],
            "apple-icon-144x144.png":     [144, 144],
            "apple-icon-152x152.png":     [152, 152],
            "apple-icon-180x180.png":     [180, 180],
            "apple-icon-57x57.png":       [57, 57],
            "apple-icon-60x60.png":       [60, 60],
            "apple-icon-72x72.png":       [72, 72],
            "apple-icon-76x76.png":       [76, 76],
            "apple-icon-precomposed.png": [192, 192],
            "favicon-16x16.png":          [16, 16],
            "favicon-32x32.png":          [32, 32],
            "favicon-96x96.png":          [96, 96],
            "ms-icon-144x144.png":        [144, 144],
            "ms-icon-150x150.png":        [150, 150],
            "ms-icon-310x310.png":        [310, 310],
            "ms-icon-70x70.png":          [70, 70],
        }

        self.parser = self.argparser()

    def make_dirs(self):
        """Create output and tmp directories"""
        if not os.path.isdir(self.tmp_path):
            os.makedirs(self.tmp_path)

        if not os.path.isdir(self.output_path):
            os.makedirs(self.output_path)

    def remove_dirs(self):
        """Remove output and tmp directories"""
        if os.path.isdir(self.tmp_path):
            rmtree(self.tmp_path)

        if os.path.isdir(self.output_path):
            rmtree(self.output_path)

    @staticmethod
    def argparser():
        """Create Argument Parser
        :returns argparse.ArgumentParser()
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("file", nargs='?', help="Source PNG file")
        return parser

    def get_filename(self):
        """Get first argument as file name"""
        filename = self.parser.parse_args().file

        if filename is None:
            sys.exit("Error: Please provide a file")

        if not os.path.isfile(filename):
            sys.exit("Error: File not found")

        return filename

    @staticmethod
    def resize(image, size, fmt="PNG"):
        """Resize image
        :param image: Image, image object
        :param size: List
        :returns: Image object
        :rtype: Image
        """
        image_copy = image.copy()
        image_copy.thumbnail((size[0], size[1]), Image.BICUBIC)
        new_image = Image.new('RGBA', (size[0], size[1]), (255, 255, 255, 0))
        position = (
            int(math.ceil((size[0] - image_copy.size[0]) / 2)),
            int(math.ceil((size[1] - image_copy.size[1]) / 2))
        )
        new_image.paste(image_copy, position)
        new_image.format = fmt
        return new_image.convert('RGBA')

    def create_extras(self):
        """Create extra files"""
        with open(os.path.join(self.tmp_path, 'browserconfig.xml'), "w") as extra_file:
            extra_file.write(extras.BROWSERCONFIG_XML)

        with open(os.path.join(self.tmp_path, 'manifest.json'), "w") as extra_file:
            extra_file.write(extras.MANIFEST_JSON)

        with open(os.path.join(self.tmp_path, 'html.txt'), "w") as extra_file:
            extra_file.write(extras.HTML_TXT)

    def process(self):
        """Create required folders, files and resize images"""
        with Image.open(self.get_filename()) as image:
            if not image.format == 'PNG':
                sys.exit("Error: Not a PNG file")

            self.make_dirs()
            self.create_extras()

            for filename, size in self.icons.items():
                icon_image = self.resize(image, size)
                icon_image.save(os.path.join(self.tmp_path, filename))

            icon_image = self.resize(image, [16, 16], "ICO")
            icon_image.save(os.path.join(self.tmp_path, "favicon.ico"))

    def create_zip(self):
        """Pack generated images as zip file"""
        zip_name = datetime.datetime.now().strftime("%Y-%m-%d-%H%I%S")
        make_archive(os.path.join(self.output_path, zip_name), "zip", "tmp")
        message = "Success! Please check {} directory for generated zip file " \
                  "({}.zip) or {} directory for unzipped files "
        sys.exit(message.format(self.output_dir, zip_name, self.tmp_dir))


if __name__ == "__main__":
    FAVIGEN = Favigen()
    FAVIGEN.process()
    FAVIGEN.create_zip()
