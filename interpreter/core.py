from .runtime import process_line

def run_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    context = {}  # shared context between all lines

    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue
        i = process_line(line, lines, i, context)  # pass context
        i += 1
