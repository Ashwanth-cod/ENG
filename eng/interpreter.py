import sys
import json

variables = {}
functions = {}

class ReturnValue(Exception):
    def __init__(self, value):
        self.value = value

class BreakLoop(Exception): pass
class ContinueLoop(Exception): pass

def evaluate_expression(expr, local_vars=None):
    scope = (local_vars or variables).copy()
    for k, v in scope.items():
        if isinstance(v, str):
            try:
                scope[k] = int(v)
            except ValueError:
                try:
                    scope[k] = float(v)
                except ValueError:
                    pass
    try:
        return eval(expr, {}, scope)
    except Exception:
        return expr

def process_block(lines, index):
    block = []
    while index < len(lines):
        line = lines[index]
        if line.startswith("  "):  # indent = block
            block.append(line.strip())
            index += 1
        else:
            break
    return block, index

def skip_conditional(lines, index, allowed):
    while index < len(lines):
        line = lines[index]
        if any(line.strip().startswith(k) for k in allowed):
            return index
        elif not line.startswith("  "):
            break
        index += 1
    return index

def process_line(line, lines, index, local_vars=None):
    if line.startswith("ask "):
        prompt = line.split('"')[1]
        parts = line.split("save as")
        var = parts[1].strip()
        value = input(prompt + " ")
        try:
            value = int(value)
        except:
            try:
                value = float(value)
            except:
                pass
        (local_vars or variables)[var] = value

    elif line.startswith("say "):
        expr = line[4:].strip()
        try:
            output = evaluate_expression(expr, local_vars)
            print(output)
        except:
            print(expr)

    elif line.startswith("let "):
        var_expr = line[4:].split(" be ")
        var = var_expr[0].strip()
        expr = var_expr[1].strip()
        value = evaluate_expression(expr, local_vars)
        (local_vars or variables)[var] = value

    elif line.startswith("if "):
        condition = line[3:].strip()
        if evaluate_expression(condition, local_vars):
            block, new_index = process_block(lines, index + 1)
            for bline in block:
                process_line(bline, lines, 0, local_vars)
            return new_index - 1
        else:
            return skip_conditional(lines, index + 1, ["elif", "else"]) - 1

    elif line.startswith("elif "):
        condition = line[5:].strip()
        if evaluate_expression(condition, local_vars):
            block, new_index = process_block(lines, index + 1)
            for bline in block:
                process_line(bline, lines, 0, local_vars)
            return new_index - 1
        else:
            return skip_conditional(lines, index + 1, ["elif", "else"]) - 1

    elif line.startswith("else"):
        block, new_index = process_block(lines, index + 1)
        for bline in block:
            process_line(bline, lines, 0, local_vars)
        return new_index - 1

    elif line.startswith("define "):
        fn_name = line.split("define ")[1].strip()
        block, new_index = process_block(lines, index + 1)
        functions[fn_name] = block
        return new_index - 1

    elif line.startswith("call "):
        parts = line.split()
        fn_name = parts[1]
        args = [evaluate_expression(arg.strip(), local_vars) for arg in parts[2:]] if len(parts) > 2 else []
        result = call_function(fn_name, args)
        (local_vars or variables)["_"] = result

    elif line.startswith("return "):
        expr = line[7:].strip()
        raise ReturnValue(evaluate_expression(expr, local_vars))

    elif line.startswith("repeat "):
        count = int(evaluate_expression(line.split()[1], local_vars))
        block, new_index = process_block(lines, index + 1)
        try:
            for _ in range(count):
                for bline in block:
                    try:
                        process_line(bline, lines, 0, local_vars)
                    except ContinueLoop:
                        break
        except BreakLoop:
            pass
        return new_index - 1

    elif line.startswith("while "):
        condition = line[6:].strip()
        block, new_index = process_block(lines, index + 1)
        try:
            while evaluate_expression(condition, local_vars):
                for bline in block:
                    try:
                        process_line(bline, lines, 0, local_vars)
                    except ContinueLoop:
                        break
        except BreakLoop:
            pass
        return new_index - 1

    elif line.strip() == "break":
        raise BreakLoop()

    elif line.strip() == "continue":
        raise ContinueLoop()

    elif line.startswith("savejson "):
        filename = line.split(" ")[1].strip()
        with open(filename, "w") as f:
            json.dump(variables, f)
        print(f"Variables saved to {filename}")

    elif line.startswith("loadjson "):
        filename = line.split(" ")[1].strip()
        with open(filename, "r") as f:
            loaded = json.load(f)
            variables.update(loaded)
        print(f"Variables loaded from {filename}")

    return index

def call_function(name, args):
    block = functions.get(name, [])
    local_vars = {f"arg{i}": arg for i, arg in enumerate(args)}
    try:
        for line in block:
            process_line(line, block, 0, local_vars)
    except ReturnValue as rv:
        return rv.value
    return None

def run_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    index = 0
    while index < len(lines):
        line = lines[index].rstrip('\n')
        if not line.strip() or line.strip().startswith("#"):
            index += 1
            continue
        new_index = process_line(line.strip(), lines, index)
        index = new_index + 1

def run_repl():
    print("Welcome to the ENG REPL! Type 'exit' or press Ctrl+C to quit.\n")
    buffer = []
    while True:
        try:
            prompt = "... " if buffer else ">>> "
            line = input(prompt)
            if line.strip() == "exit":
                break
            if line.strip() == "":
                for i in range(len(buffer)):
                    lines = buffer.copy()
                    process_line(lines[i].strip(), lines, i)
                buffer.clear()
            else:
                buffer.append(line)
        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"Error: {e}")
            buffer.clear()

def main():
    if len(sys.argv) >= 2:
        run_file(sys.argv[1])
    else:
        run_repl()

if __name__ == "__main__":
    main()
