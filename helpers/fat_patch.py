import fs
from pathlib import Path
from pyfatfs import PyFatFS
from fontTools import ttLib, subset
import base64
import io
import sys
import os

fat = PyFatFS.PyFatFS("./rsrc.bin", read_only=False)
print(fat.listdir('/Resources/UI'))

FONT_BASE = "/Resources/Fonts/"
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


for root, dirs, files in os.walk("./Fonts"):
    for file in files:
        if file.endswith(".ttf"):
            print("Processing " + file + "...")
            custom_ttf_path = os.path.join(root, file)

            # Read the file, get its name
            system_ttf_path = os.path.join(FONT_BASE, file)
            try:
                b = fat.openbin(system_ttf_path, mode="rb")
                original_font = ttLib.TTFont(b)
                original_font_name_table = original_font["name"]
                b.close()

                # Remove the old font
                fat.remove(system_ttf_path)

                # Open the file to write our font
                b = fat.openbin(system_ttf_path, mode="wb")

                with open(custom_ttf_path, "rb") as f:
                    fake_font = ttLib.TTFont(f)
                    fake_font["name"] = original_font_name_table
                    print("Replacing " + file +"...")
                    fake_font.save(b)

                b.close()
            except Exception as e:
                print(f"An error occurred while opening {system_ttf_path}: {e}")

if os.path.exists("./SilverImagesDB.LE.bin2"):
    fat.remove(IMAGE_BASE)
    b = fat.openbin(IMAGE_BASE, mode="wb")
    with open("./SilverImagesDB.LE.bin2", "rb") as local_file:
        file_data = local_file.read()
        print("Replacing SilverImagesDB...")
        b.write(file_data)
    b.close()
else:
    print("Re-packed SilverImagesDB.LE.bin2 doesn't exist yet, this run is for extraction only")

if os.path.exists("./SilverDB.en_GB.LE.bin2"):
    fat.remove(EN_BASE)
    b = fat.openbin(EN_BASE, mode="wb")
    with open("./SilverDB.en_GB.LE.bin2", "rb") as local_file:
        file_data = local_file.read()
        print("Replacing SilverDB...")
        b.write(file_data)
    b.close()
else:
    print("Re-packed SilverDB.en_GB.LE.bin2 doesn't exist yet, this run is for extraction only")

fat.close()
