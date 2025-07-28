from process import parse_file, get_paths, count_letters_in_text, merge_results
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm
from dataclasses import asdict
from result import Result
from letter_context import LetterContext
import string

import json

def context_map_to_dict(context_map):
    return {
        ch: {
            "before": context.before,
            "after": context.after
        }
        for ch, context in context_map.items()
    }

context_map: dict[str, LetterContext] = {
    ch: LetterContext() for ch in string.ascii_lowercase
}
def process_file(filepath):
    words = parse_file(filepath)
    result = count_letters_in_text(words)
    context = build_context_map(words)
    return result, context



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

from collections import defaultdict
from letter_context import LetterContext

def build_context_map(words: list[str]) -> dict[str, LetterContext]:
    local_map: dict[str, LetterContext] = {
        ch: LetterContext() for ch in string.ascii_lowercase
    }

    for word in words:
        chars = list(word.lower())
        for i, c in enumerate(chars):
            if c not in string.ascii_lowercase:
                continue

            if i > 0:
                prev = chars[i - 1]
                if prev in string.ascii_lowercase:
                    local_map[c].before[prev] += 1

            if i < len(chars) - 1:
                nxt = chars[i + 1]
                if nxt in string.ascii_lowercase:
                    local_map[c].after[nxt] += 1

    return local_map

def merge_context_maps(m1: dict[str, LetterContext], m2: dict[str, LetterContext]) -> dict[str, LetterContext]:
    for ch in string.ascii_lowercase:
        for b in string.ascii_lowercase:
            m1[ch].before[b] += m2[ch].before[b]
            m1[ch].after[b] += m2[ch].after[b]
    return m1

if __name__ == '__main__':
    paths = get_paths()
    print(f"Found {len(paths)} files.")

    master_result = Result()
    context_map: dict[str, LetterContext] = {
        ch: LetterContext() for ch in string.ascii_lowercase
    }

    with ProcessPoolExecutor(max_workers=64) as executor:
        partials = executor.map(process_file, paths, chunksize=3)
        for result, context in tqdm(partials, total=len(paths), desc="Counting Letters & Context", unit="file"):
            master_result = merge_results(master_result, result)
            context_map = merge_context_maps(context_map, context)

    print("Final Letter Frequencies (sorted):")
    for ch, count in sorted(asdict(master_result).items(), key=lambda x: -x[1]):
        print(f"{ch}: {count:,}")    

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
    
    with open("letter_context.json", "w") as f:
        json.dump(context_map_to_dict(context_map), f, indent=2)
