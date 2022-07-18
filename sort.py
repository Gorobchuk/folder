import sys
from pathlib import Path
from typing import Container

from pip import main
JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
MY_OTHER = []
ARCHIVES = []
REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'ZIP': ARCHIVES
}
FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()

def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper()
    def scan(folder: Path) -> None:
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                    FOLDERS.append(item)
                    scan(item)
                    continue
                ext = get_extension(item.name)
                fullname = folder / item.name
                if not ext:
                    MY_OTHER.append(fullname)
                else:
                    try:
                        container = REGISTER_EXTENSIONS[ext]
                        EXTENSIONS.add(ext)
                        Container.append(fullname)
                    except KeyError:
                        UNKNOWN.add(ext)
                        MY_OTHER.append(fullname)
                        if __name__ == '__main__':
                            folder_for_scan = sys.argv[1]
                            print(f'Start in folder {folder_for_scan}')
                            scan(Path(folder_for_scan))
                            print(f'Images jpeg: {JPEG_IMAGES}')
                            print(f'Images jpg: {JPG_IMAGES}')
                            print(f'Images svg: {SVG_IMAGES}')
                            print(f'Audio mp3: {MP3_AUDIO}')
                            print(f'Archives: {ARCHIVES}')
                            print(f'Types of files in folder: {EXTENSIONS}')
                            print(f'Unknown files of types: {UNKNOWN}')
                            print(FOLDERS[::-1])

from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize
def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))
    def handle_other(filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        filename.replace(target_folder / normalize(filename.name))
        def handle_archive(filename: Path, target_folder: Path):
            target_folder.mkdir(exist_ok=True, parents=True)
            folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))
            folder_for_file.mkdir(exist_ok=True, parents=True)
            try:
                shutil.unpack_archive(str(filename.resolve()),
                str(folder_for_file.resolve()))
            except shutil.ReadError:
                print(f'Це не архів {filename}!')
                folder_for_file.rmdir()
                return None
                filename.unlink()
                def handle_folder(folder: Path):
                    try:
                        folder.rmdir()
                    except OSError:
                        print(f'Помилка видалення папки {folder}')
                        def main(folder: Path):
                            parser.scan(folder)
                            for file in parser.JPEG_IMAGES:
                                handle_media(file, folder / 'images' / 'JPEG')
                                for file in parser.JPG_IMAGES:
                                    handle_media(file, folder / 'images' / 'JPG')
                                    for file in parser.PNG_IMAGES:
                                        handle_media(file, folder / 'images' / 'PNG')
                                        for file in parser.SVG_IMAGES:
                                            handle_media(file, folder / 'images' / 'SVG')
                                            for file in parser.MP3_AUDIO:
                                                handle_media(file, folder / 'audio' / 'MP3')
                                                for file in parser.MY_OTHER:
                                                    handle_other(file, folder / 'MY_OTHER')
                                                    for file in parser.ARCHIVES:
                                                        handle_archive(file, folder / 'archives')
                                                        for folder in parser.FOLDERS[::-1]:
                                                            handle_folder(folder)
                                                            if __name__ == '__main__':
                                                                if sys.argv[1]:
                                                                    folder_for_scan = Path(sys.argv[1])
                                                                    print(f'Start in folder {folder_for_scan.resolve()}')
                                                                    main(folder_for_scan.resolve())

import re

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u", "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
    def normalize(name: str) -> str:
        t_name = name.translate(TRANS)
        t_name = re.sub(r'\W', '_', t_name)
        return t_name