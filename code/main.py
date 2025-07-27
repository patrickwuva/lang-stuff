from process import parse_file, get_paths, count_letters_in_text
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from dataclasses import asdict

if __name__ == '__main__':
    paths = get_paths()
    print(f"Found {len(paths)} files.")

    total_words = 0
    """
    with ProcessPoolExecutor(max_workers=64) as executor:
        results = executor.map(parse_file, paths, chunksize=3)
        for word_count in tqdm(results, total=len(paths), desc="Parsing", unit="file"):
            total_words += word_count
    """
    text = parse_file(paths[0])
    r = count_letters_in_text(text)
    #print(f"Total words: {total_words}")
    print(asdict(r))
