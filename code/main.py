from glob import glob

from process import parse_file, get_paths

if __name__ == '__main__':
    paths = get_paths()
    print(len(paths))
