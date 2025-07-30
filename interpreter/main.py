from .runtime import process_line

def run_file(filename):
    with open(filename, "r") as f:
        lines = [line.rstrip("\n") for line in f]

    context = {}
    env = {}
    i = 0

    def get_block(start):
        block = [lines[start]]
        indent = len(lines[start]) - len(lines[start].lstrip())
        for j in range(start + 1, len(lines)):
            line_indent = len(lines[j]) - len(lines[j].lstrip())
            if lines[j].strip() == "end" or line_indent > indent:
                block.append(lines[j])
                if lines[j].strip() == "end":
                    return block, j
            else:
                break
        return block, start

    while i < len(lines):
        line = lines[i].strip()
        if not line or line.startswith("#"):
            i += 1
            continue

        if any(line.startswith(kw) for kw in ["if ", "repeat", "define "]):
            block, new_index = get_block(i)
            process_line(block, lines, i, context, env)
            i = new_index + 1
        else:
            process_line([lines[i]], lines, i, context, env)
            i += 1
