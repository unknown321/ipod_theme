import fs
from pyfatfs import PyFatFS
from fontTools import ttLib, subset
import base64
import io
import sys
import os

fat = PyFatFS.PyFatFS("./rsrc.bin", read_only=False)
print(fat.listdir('/Resources/UI'))

FONT_BASE = "/Resources/Fonts/Helvetica.ttf"
IMAGE_BASE = "/Resources/UI/SilverImagesDB.LE.bin"
EN_BASE = "/Resources/UI/SilverDB.en_GB.LE.bin"

with fat.openbin(IMAGE_BASE, mode="rb") as b:
    file_content = b.read()
    with open("./SilverImagesDB.LE.bin", 'wb') as output_file:
        output_file.write(file_content)

with fat.openbin(EN_BASE, mode="rb") as b:
    file_content = b.read()
    with open("./SilverDB.en_GB.LE.bin", 'wb') as output_file:
        output_file.write(file_content)

'''
# Read the file, get its name
b = fat.openbin(FONT_BASE, mode="rb")
original_font = ttLib.TTFont(b)
original_font_name_table = original_font["name"]
b.close()

# Remove the old font
fat.remove(FONT_BASE)

# Open the file to write our font
b = fat.openbin(FONT_BASE, mode="wb")

with open("./in-otf.bin", "rb") as f:
    fake_font = ttLib.TTFont(f)
    fake_font["name"] = original_font_name_table
    fake_font["CFF "].cff[0].CharStrings["space"].calcBounds = lambda x: None

    fake_font.save(b)

b.close()
'''

if os.path.exists("./SilverImagesDB.LE.bin2"):
    fat.remove(IMAGE_BASE)
    b = fat.openbin(IMAGE_BASE, mode="wb")
    with open("./SilverImagesDB.LE.bin2", "rb") as local_file:
        file_data = local_file.read()
        b.write(file_data)
    b.close()
else:
    print("Re-packed SilverImagesDB.LE.bin2 doesn't exist yet, this run is for extraction only")

if os.path.exists("./SilverDB.en_GB.LE.bin2"):
    fat.remove(EN_BASE)
    b = fat.openbin(EN_BASE, mode="wb")
    with open("./SilverDB.en_GB.LE.bin2", "rb") as local_file:
        file_data = local_file.read()
        b.write(file_data)
    b.close()
else:
    print("Re-packed SilverDB.en_GB.LE.bin2 doesn't exist yet, this run is for extraction only")

fat.close()
