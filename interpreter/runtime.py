from .evaluator import evaluate_expression

functions = {}

def process_line(block, lines, index, context, env):
    stripped = block[0].strip()

    if stripped.startswith("say "):
        expr = stripped[4:].strip()
        try:
            result = evaluate_expression(expr, context)
            print(result)
        except Exception as e:
            print(f"Error in say: {e}")

    elif stripped.startswith("let "):
        code = stripped[4:].strip()
        if "=" in code:
            name_part, expr_part = code.split("=", 1)
            name = name_part.strip()
            expr = expr_part.strip()

            if expr.startswith("input "):
                try:
                    parts = expr[6:].strip().split(None, 1)
                    if len(parts) == 2:
                        prompt_raw, type_str = parts
                    else:
                        prompt_raw = parts[0]
                        type_str = "str"

                    prompt = prompt_raw.strip('"').strip("'")
                    type_str = type_str.lower()
                    raw_value = input(prompt + ": ").strip()

                    if type_str == "int":
                        value = int(raw_value)
                    elif type_str == "float":
                        value = float(raw_value)
                    elif type_str == "bool":
                        low = raw_value.lower()
                        if low in ["yes", "true"]:
                            value = True
                        elif low in ["no", "false"]:
                            value = False
                        else:
                            raise ValueError("Expected yes/true or no/false")
                    else:
                        value = raw_value

                    context[name] = value
                    env[name] = value
                except Exception as e:
                    print(f"Input error for '{name}': {e}")
            else:
                try:
                    value = evaluate_expression(expr, context)
                    context[name] = value
                    env[name] = value
                except Exception as e:
                    print(f"Assignment error for '{name}': {e}")
        else:
            print("Syntax error: missing '=' in let statement")

    elif stripped.startswith("if ") and stripped.endswith(":"):
        condition = stripped[3:-1].strip()
        try:
            if evaluate_expression(condition, context):
                for line in block[1:-1]:
                    process_line([line.strip()], lines, index, context, env)
        except Exception as e:
            print(f"Error in if block: {e}")

    elif stripped.startswith("repeat") and "times" in stripped:
        header = stripped.replace("repeat", "").replace("times:", "").strip()
        try:
            times = int(evaluate_expression(header, context))
            for _ in range(times):
                for line in block[1:-1]:
                    process_line([line.strip()], lines, index, context, env)
        except Exception as e:
            print(f"Error in repeat block: {e}")

    elif stripped.startswith("define ") and stripped.endswith(":"):
        header = stripped[7:-1].strip()
        func_name, arg_str = header.split("(", 1)
        func_name = func_name.strip()
        args = [a.strip() for a in arg_str.strip(")").split(",") if a.strip()]
        body = block[1:-1]
        functions[func_name] = (args, body)

    elif stripped.startswith("call "):
        try:
            expr = stripped[5:].strip()
            evaluate_expression(expr, context)  # supports .append(), .get(), etc.
        except Exception as e:
            print(f"Function call error: {e}")

    elif stripped == "end":
        return
