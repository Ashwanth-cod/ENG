from .main import run_file

import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m interpreter <filename>")
    else:
        run_file(sys.argv[1])
