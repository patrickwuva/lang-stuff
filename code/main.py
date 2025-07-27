from process import parse_file, get_paths, count_letters_in_text, merge_results
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from dataclasses import asdict
from result import Result

def process_file(filepath):
    words = parse_file(filepath)
    return count_letters_in_text(words)

if __name__ == '__main__':
    paths = get_paths()
    print(f"Found {len(paths)} files.")

    master_result = Result()

    with ProcessPoolExecutor(max_workers=64) as executor:
        partial_results = executor.map(process_file, paths, chunksize=3)
        for r in tqdm(partial_results, total=len(paths), desc="Counting Letters", unit="file"):
            master_result = merge_results(master_result, r)

    sorted_counts = sorted(asdict(master_result).items(), key=lambda x: -x[1])

    print("Final Letter Frequencies (sorted):")
    for ch, count in sorted_counts:
        print(f"{ch}: {count:,}")    

