import re
import os
from word import Word
from result import Result
import string


def get_paths(root_dir='/home/tpv/Random/Lang/datasets/fullEnglish'):
    all_paths = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            all_paths.append(full_path)
    return all_paths


word_re = re.compile(r"\b\w+\b")

def parse_file(filepath):
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return word_re.findall(text.lower())



def count_letters_in_text(text: str) -> Result:
    result = Result()
    for raw_word in text.split():
        word = Word.from_string(raw_word.lower())  # Normalize to lowercase
        for ch in word.get_chars():
            if ch in string.ascii_lowercase:  # Only count a-z
                setattr(result, ch, getattr(result, ch) + 1)
    return result

