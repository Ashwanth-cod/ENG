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
    scope = variables.copy()
    if local_vars:
        scope.update(local_vars)
    for var in scope:
        expr = expr.replace(var, repr(scope[var]))
    try:
        return eval(expr)
    except:
        return expr

def process_block(lines, index):
    block = []
    while index < len(lines):
        line = lines[index]
        if line.startswith("  "):  # indented block
            block.append(line.strip())
            index += 1
        else:
            break
    return block, index

def process_line(line, local_vars=None):
    global current_index

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
            output = eval(expr, {}, local_vars or variables)
            print(output)
        except:
            parts = expr.split("+")
            output = ""
            for part in parts:
                part = part.strip()
                if part.startswith('"') and part.endswith('"'):
                    output += part[1:-1]
                elif part in (local_vars or variables):
                    output += str((local_vars or variables)[part])
                else:
                    output += part
            print(output)

    elif line.startswith("let "):
        var_expr = line[4:].split(" be ")
        var = var_expr[0].strip()
        expr = var_expr[1].strip()
        value = evaluate_expression(expr, local_vars)
        (local_vars or variables)[var] = value

    elif line.startswith("if "):
        condition = line[3:].strip()
        if " is " in condition:
            var, value = condition.split(" is ")
            var = var.strip()
            value = value.strip().strip('"')
            if str((local_vars or variables).get(var)) == value:
                block, new_index = process_block(current_lines, current_index + 1)
                for bline in block:
                    process_line(bline, local_vars)
                current_index = new_index
            else:
                skip_conditional(["elif", "else"])

    elif line.startswith("elif "):
        condition = line[5:].strip()
        if " is " in condition:
            var, value = condition.split(" is ")
            var = var.strip()
            value = value.strip().strip('"')
            if str((local_vars or variables).get(var)) == value:
                block, new_index = process_block(current_lines, current_index + 1)
                for bline in block:
                    process_line(bline, local_vars)
                current_index = new_index
            else:
                skip_conditional(["elif", "else"])

    elif line.startswith("else"):
        block, new_index = process_block(current_lines, current_index + 1)
        for bline in block:
            process_line(bline, local_vars)
        current_index = new_index

    elif line.startswith("define "):
        fn_name = line.split("define ")[1].strip()
        block, new_index = process_block(current_lines, current_index + 1)
        functions[fn_name] = block
        current_index = new_index

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
        block, new_index = process_block(current_lines, current_index + 1)
        try:
            for _ in range(count):
                for bline in block:
                    process_line(bline, local_vars)
        except BreakLoop:
            pass
        current_index = new_index

    elif line.startswith("while "):
        condition = line[6:].strip()
        block, new_index = process_block(current_lines, current_index + 1)
        try:
            while eval(condition, {}, local_vars or variables):
                for bline in block:
                    process_line(bline, local_vars)
        except BreakLoop:
            pass
        current_index = new_index

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

def skip_conditional(allowed):
    global current_index
    index = current_index + 1
    while index < len(current_lines):
        line = current_lines[index]
        if any(line.strip().startswith(k) for k in allowed):
            current_index = index
            return
        elif not line.startswith("  "):
            break
        index += 1
    current_index = index

def call_function(name, args):
    block = functions.get(name, [])
    local_vars = {f"arg{i}": arg for i, arg in enumerate(args)}
    try:
        for line in block:
            process_line(line, local_vars)
    except ReturnValue as rv:
        return rv.value
    return None

def run_file(filename):
    global current_lines, current_index
    with open(filename, 'r') as f:
        current_lines = f.readlines()
    current_index = 0
    while current_index < len(current_lines):
        line = current_lines[current_index].rstrip('\n')
        if not line.strip() or line.strip().startswith("#"):
            current_index += 1
            continue
        process_line(line.strip())
        current_index += 1

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
                for i, line in enumerate(buffer):
                    global current_lines, current_index
                    current_lines = buffer
                    current_index = i
                    while current_index < len(current_lines):
                        process_line(current_lines[current_index].strip())
                        current_index += 1
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
