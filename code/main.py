from glob import glob

from process import parse_file, get_paths

if __name__ == '__main__':
    total = 0
    paths = get_paths()
    print(len(paths))
    for path in paths:
        words = parse_file(paths)
        total += len(words)

    print(f'total words: {total}');
    
