import sys
from .core import run_file

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m interpreter <filename.eng>")
        return
    run_file(sys.argv[1])
