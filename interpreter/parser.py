def group_blocks(lines):
    blocks = []
    current_block = []
    indent_level = 0

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        if stripped.startswith(("if ", "repeat", "define")) and stripped.endswith(":"):
            if current_block:
                blocks.append(current_block)
            current_block = [line.strip()]
            indent_level = len(line) - len(line.lstrip())

        elif stripped == "end":
            current_block.append(line.strip())
            blocks.append(current_block)
            current_block = []
            indent_level = 0

        elif current_block:
            current_block.append(line.strip())

        else:
            blocks.append([line.strip()])

    if current_block:
        blocks.append(current_block)

    return blocks
