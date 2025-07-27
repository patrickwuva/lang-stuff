from glob import glob

from process import parse_file, get_paths
from concurrent.futures import ProcessPoolExecutor


if __name__ == '__main__':
    paths = get_paths()
    print(f"Found {len(paths)} files.")

    total_words = 0
    with ProcessPoolExecutor() as executor:
        for words in executor.map(parse_file, paths):
            total_words += len(words)

    print(f"Total words: {total_words}")

