def collect_block(lines, start_index):
    block = [lines[start_index]]
    i = start_index + 1
    while i < len(lines):
        line = lines[i].strip()
        block.append(lines[i])
        if line == "end":
            break
        i += 1
    return block, i + 1
