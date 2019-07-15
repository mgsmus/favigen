from PIL import Image
from shutil import make_archive, copy
from pathlib import Path
import argparse
import sys
import os
import math
import datetime

icons = {
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

BASE_PATH = str(Path(__file__).resolve().parent)

TMP_DIR = "tmp"
OUTPUT_DIR = "output"
DATA_DIR = "data"
TMP_PATH = "{}/{}".format(BASE_PATH, TMP_DIR)
OUTPUT_PATH = "{}/{}".format(BASE_PATH, OUTPUT_DIR)
DATA_PATH = "{}/{}".format(BASE_PATH, DATA_DIR)

if not os.path.isdir(TMP_PATH):
    os.makedirs(TMP_PATH)

if not os.path.isdir(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

parser = argparse.ArgumentParser()
parser.add_argument("file", nargs='?', help="Source PNG file")

file = parser.parse_args().file

if file is None:
    sys.exit("Error: Please provide a file")

if not os.path.isfile(file):
    sys.exit("Error: File not found")


def resize(image, size, format="PNG"):
    im = image.copy()
    im.thumbnail((size[0], size[1]), Image.BICUBIC)
    bg = Image.new('RGBA', (size[0], size[1]), (255, 255, 255, 0))
    position = (
        int(math.ceil((size[0] - im.size[0]) / 2)),
        int(math.ceil((size[1] - im.size[1]) / 2))
    )
    bg.paste(im, position)
    bg.format = format
    return bg.convert('RGBA')


with Image.open(file) as image:
    if not image.format == 'PNG':
        sys.exit("Error: Not a PNG file")

    for filename, size in icons.items():
        im = resize(image, size)
        im.save("{}/{}".format(TMP_PATH, filename))

    im = resize(image, [16, 16], "ICO")
    im.save("{}/favicon.ico".format(TMP_PATH))

copy("{}/browserconfig.xml".format(DATA_PATH), "{}/browserconfig.xml".format(TMP_PATH))
copy("{}/manifest.json".format(DATA_PATH), "{}/manifest.json".format(TMP_PATH))
copy("{}/readme.txt".format(DATA_PATH), "{}/readme.txt".format(TMP_PATH))

zip_name = datetime.datetime.now().strftime("%Y-%m-%d-%H%I%S")
make_archive("{}/{}".format(OUTPUT_PATH, zip_name), "zip", "tmp")

sys.exit("Success! Please check {} directory for generated zip file ({}.zip) or {} directory for unzipped files"
         .format(OUTPUT_DIR, zip_name, TMP_DIR))
