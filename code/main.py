from glob import glob
from process import parse_file, get_paths
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

if __name__ == '__main__':
    paths = get_paths()
    print(f"Found {len(paths)} files.")

    total_words = 0
    with ThreadPoolExecutor(max_workers=64) as executor:
        for words in tqdm(executor.map(parse_file, paths), total=len(paths)):
            total_words += len(words)

    print(f"Total words: {total_words}")

