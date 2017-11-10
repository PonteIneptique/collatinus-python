"""

This script is responsible for the update of source data of PyCollatinus.

.. author:: Thibault Clérice (@ponteineptique)
"""
from io import BytesIO
from zipfile import ZipFile
from urllib3 import PoolManager
import glob

# Setting up the list of file to update
files = [
    (file, file.replace("pycollatinus/data", "collatinus-master/bin/data"))
    for file in glob.glob("pycollatinus/data/*.*")
    if not file.endswith(".pickle")
]

print("Contacting Github")
http = PoolManager()
url = http.request("GET", "https://github.com/biblissima/collatinus/archive/master.zip")
print("Reading zip")
zipfile = ZipFile(BytesIO(url.data))
for target, source in files:
    print("\tUpdating {}".format(target))
    with zipfile.open(source) as source_io:
        with open(target, "w") as target_io:
            target_io.write(
                source_io.read().decode()
                    .replace("ho!|inv|||interj.|1", "ho|inv|||interj.|1")  # Known line that creates bug in PyCollatinus
            )

print("Done")