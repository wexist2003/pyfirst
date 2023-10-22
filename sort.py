import sys
import os
from pathlib import Path


def normalize(name):
    pass
    return


appends = {
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".z", ".tar"],
}

path = Path(sys.argv[1])
try:
    for folder, append in appends.items():
        os.mkdir(f"{path}\{folder}")
except:
    pass

for file in path.iterdir():
    for folder, append in appends.items():
        if file.suffix in append:
            os.rename(file, f"{path}\{folder}")
