import sys
import os
import shutil
from pathlib import Path


# translate
def normalize(name):
    name_translit = name.replace(r'[^a-zA-Z0-9]', '_')
    print(name_translit)
    CYRILLIC = (
        "а",
        "б",
        "в",
        "г",
        "д",
        "е",
        "ё",
        "ж",
        "з",
        "и",
        "й",
        "к",
        "л",
        "м",
        "н",
        "о",
        "п",
        "р",
        "с",
        "т",
        "у",
        "ф",
        "х",
        "ц",
        "ч",
        "ш",
        "щ",
        "ь",
        "ы",
        "ъ",
        "э",
        "ю",
        "я",
        "є",
        "і",
        "ї",
        "ґ",
    )
    LATIN = (
        "a",
        "b",
        "v",
        "g",
        "d",
        "e",
        "yo",
        "zh",
        "dz",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "r",
        "s",
        "t",
        "u",
        "f",
        "h",
        "c",
        "ch",
        "sh",
        "sch",
        "j",
        "y",
        "j",
        "e",
        "u",
        "ja",
        "_",
        "_",
        "_",
        "_",
    )

    TRANSLIT_DICT = {}

    for c, l in zip(CYRILLIC, LATIN):
        TRANSLIT_DICT[ord(c)] = l
        TRANSLIT_DICT[ord(c.upper())] = l.upper()

    name_translit = name_translit.translate(TRANSLIT_DICT)

    return name_translit


def renamer_ff(path):
    for file in path.iterdir():
        name_x = file.name
        suffix = file.suffix
        new_name = normalize(name_x.removesuffix(suffix))
        if file.is_dir():
            sub_dir_path = f"{path}\{new_name}"
            os.rename(file, sub_dir_path)
            renamer_ff(Path(sub_dir_path))
        else:
            new_file_name = f"{path}\{new_name}{suffix}"
            os.rename(file, new_file_name)


path = Path("c:\\Users\\wexist\\Desktop\\PYTH2\\")
renamer_ff(path)
