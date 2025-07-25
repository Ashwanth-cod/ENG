from .runtime import process_line
from .core import collect_block

def run_file(filepath):
    with open(filepath, 'r') as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    context = {}
    env = {}
    index = 0

    while index < len(lines):
        line = lines[index].strip()
        if not line or line.startswith("#"):
            index += 1
            continue

        block, next_index = collect_block(lines, index)
        process_line(block, lines, index, context, env)
        index = next_index
