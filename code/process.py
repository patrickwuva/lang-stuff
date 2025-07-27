import re
import os


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
    return len(word_re.findall(text.lower()))

