from process import parse_file, get_paths
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

if __name__ == '__main__':
    paths = get_paths()
    print(f"Found {len(paths)} files.")

    total_words = 0
    with ProcessPoolExecutor(max_workers=64) as executor:  # Use 64 if you want full saturation
        futures = [executor.submit(parse_file, path) for path in paths]

        for future in tqdm(as_completed(futures), total=len(futures), desc="Parsing", unit="file"):
            try:
                words = future.result()
                total_words += len(words)
            except Exception as e:
                print(f"Error: {e}")

    print(f"Total words: {total_words}")

