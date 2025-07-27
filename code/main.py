from process import parse_file, get_paths
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

if __name__ == '__main__':
    paths = get_paths()
    print(f"Found {len(paths)} files.")

    total_words = 0
    with ProcessPoolExecutor(max_workers=64) as executor:
        results = executor.map(parse_file, paths, chunksize=10)
        for word_count in tqdm(results, total=len(paths), desc="Parsing", unit="file"):
            total_words += word_count

    print(f"Total words: {total_words}")

