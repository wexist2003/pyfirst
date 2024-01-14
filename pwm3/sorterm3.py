import os
from concurrent.futures import ThreadPoolExecutor
import shutil

# file worker
def process_file(file_path):
    _, file_extension = os.path.splitext(file_path)
    dest_folder = os.path.join(source_folder, file_extension[1:])
    os.makedirs(dest_folder, exist_ok=True)
    dest_path = os.path.join(dest_folder, os.path.basename(file_path))
    shutil.move(file_path, dest_path)

# thread
def process_folder(folder):
    with ThreadPoolExecutor() as executor:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                executor.submit(process_file, file_path)

    # delete dir 0 files
    for root, dirs, _ in os.walk(folder, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

if __name__ == "__main__":
    source_folder = input("Input sorse folder?")
    process_folder(source_folder)

