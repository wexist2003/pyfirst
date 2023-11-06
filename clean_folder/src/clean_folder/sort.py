import sys
import os
import shutil
from pathlib import Path


# z-folder
def del_empty_dirs(path):
    for way in os.listdir(path):
        source = os.path.join(path, way)
        if os.path.isdir(source):
            del_empty_dirs(source)
            if not os.listdir(source):
                os.rmdir(source)


# sorter
def iter_dir(path, dist_folders):
    for file in path.iterdir():
        for folder, append in appends.items():
            if file.suffix in append:
                if folder == "archives":
                    try:
                        name = file.name.removesuffix(file.suffix)
                        shutil.unpack_archive(file, f"{dist_folders}\\{folder}\\{name}")
                        # renamer_ff(f"{dist_folders}\{folder}")
                        os.remove(file)
                    except:
                        continue
                else:
                    shutil.move(
                        file, f"{dist_folders}\\{folder}\\{file.name}{file.suffix}"
                    )
        if file.is_dir():
            n = 0
            for folder, append in appends.items():
                if folder == file.name:
                    n += 1
            if n == 0:
                iter_dir(file, dist_folders)


def main(*argv):
    path = Path(sys.argv[1])
    # renaming
    renamer_ff(path)

    # create dist folders
    for folder, append in appends.items():
        try:
            os.mkdir(f"{path}\\{folder}")
        except:
            continue

    # take current files in dir and sorting
    iter_dir(path, path)

    # delete free dirs
    del_empty_dirs(path)


# transliterator
def normalize(name):
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
        "/",
        "*",
        "-",
        "\\",
        ",",
        ".",
        "?",
        ">",
        "<",
        "[",
        "]",
        "{",
        "}",
        "+",
        "&",
        "^",
        "%",
        "$",
        "#",
        "@",
        "!",
        "~",
        "'",
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
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
        "_",
    )

    TRANSLIT_DICT = {}

    for c, l in zip(CYRILLIC, LATIN):
        TRANSLIT_DICT[ord(c)] = l
        TRANSLIT_DICT[ord(c.upper())] = l.upper()

    name_translit = name.translate(TRANSLIT_DICT)

    return name_translit


# transliteration file trees
def renamer_ff(path):
    for file in path.iterdir():
        name_x = file.name
        suffix = file.suffix
        new_name = normalize(name_x.removesuffix(suffix))
        if file.is_dir():
            sub_dir_path = f"{path}\\{new_name}"
            os.rename(file, sub_dir_path)
            renamer_ff(Path(sub_dir_path))
        else:
            new_file_name = f"{path}\\{new_name}{suffix}"
            os.rename(file, new_file_name)
    return


# suffixes
appends = {
    "images": [".jpeg", ".png", ".jpg", ".svg"],
    "video": [".avi", ".mp4", ".mov", ".mkv"],
    "documents": [".doc", ".docx", ".txt", ".pdf", ".xlsx", ".pptx"],
    "audio": [".mp3", ".ogg", ".wav", ".amr"],
    "archives": [".zip", ".z", ".tar", ".rar"],
}

list_files = {
    "images": {},
    "video": {},
    "documents": {},
    "audio": {},
    "archives": {},
    "other": {},
}

if __name__ == "__main__":
    main(sys.argv)
