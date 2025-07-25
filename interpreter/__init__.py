from .main import run_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m interpreter <file.eng>")
    else:
        run_file(sys.argv[1])
