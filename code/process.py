import re

def parse_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    words = re.findall(r"\b\w+\b", text.lower())
    return words

