from .evaluator import evaluate_expression

def process_line(line, lines, index, context):
    if line.startswith("say "):
        expr = line[4:].strip()
        result = evaluate_expression(expr, context)
        print(result)

    elif line.startswith("let "):
        parts = line[4:].split("=")
        if len(parts) != 2:
            print("Invalid let statement")
            return index
    
        left, right = parts
        var_names = [v.strip() for v in left.split(",")]
        value = evaluate_expression(right.strip(), context)
    
        if isinstance(value, tuple) or isinstance(value, list):
            if len(var_names) != len(value):
                print("Error: Number of variables and values do not match")
                return index
            for var, val in zip(var_names, value):
                context[var] = val
        else:
            if len(var_names) > 1:
                print("Error: Cannot unpack non-iterable value")
                return index
            context[var_names[0]] = value

    return index
