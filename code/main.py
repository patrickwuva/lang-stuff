from process import parse_file, get_paths, count_letters_in_text, merge_results
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from dataclasses import asdict
from result import Result
from letter_context import LetterContext
import string

context_map: dict[str, LetterContext] = {
    ch: LetterContext() for ch in string.ascii_lowercase
}
def process_file(filepath):
    words = parse_file(filepath)
    return count_letters_in_text(words)


def update_context_counts(words: list[str]):
    for word in words:
        chars = list(word.lower())
        for i, c in enumerate(chars):
            if c not in string.ascii_lowercase:
                continue

            if i > 0:
                prev = chars[i - 1]
                if prev in string.ascii_lowercase:
                    context_map[c].before[prev] += 1

            if i < len(chars) - 1:
                nxt = chars[i + 1]
                if nxt in string.ascii_lowercase:
                    context_map[c].after[nxt] += 1

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

    print("Building letter context map...")
    for path in tqdm(paths, desc="Letter Context"):
        words = parse_file(path)  # single-threaded
        update_context_counts(words)

    print("\nLetter Context Summary:")
    for letter in string.ascii_lowercase:
        ctx = context_map[letter]
        print(f"\nLetter '{letter}':")
        print("  Most common letters before:")
        for b, cnt in sorted(ctx.before.items(), key=lambda x: -x[1])[:5]:
            print(f"    {b}: {cnt:,}")
        print("  Most common letters after:")
        for a, cnt in sorted(ctx.after.items(), key=lambda x: -x[1])[:5]:
            print(f"    {a}: {cnt:,}")
