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
            print(f"Error evaluating '{expr}': {e}")

    elif stripped.startswith("let "):
        code = stripped[4:].strip()
        if "=" in code:
            name_part, expr_part = code.split("=", 1)
            name = name_part.strip()
            expr = expr_part.strip()

            if expr.startswith("input "):
                parts = expr[6:].strip().split(None, 1)
                if len(parts) == 2:
                    prompt_and_type = parts[1].rsplit(" ", 1)
                    if len(prompt_and_type) == 2:
                        prompt, type_str = prompt_and_type
                    else:
                        prompt = prompt_and_type[0]
                        type_str = "str"
                else:
                    prompt = parts[0]
                    type_str = "str"

                prompt = prompt.strip('"').strip("'")
                try:
                    raw_value = input(prompt + ": ")
                    if type_str == "int":
                        value = int(raw_value)
                    elif type_str == "float":
                        value = float(raw_value)
                    elif type_str == "bool":
                        value = True if raw_value.lower() in ["yes", "y"] else False
                    else:
                        value = raw_value
                    context[name] = value
                    env[name] = value
                except Exception as e:
                    print(f"Error during input: {e}")
            else:
                try:
                    value = evaluate_expression(expr, context)
                    context[name] = value
                    env[name] = value
                except Exception as e:
                    print(f"Error assigning '{name}': {e}")
        else:
            print("Invalid let statement")

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
            call_line = stripped[5:].strip()
            func_name, arg_str = call_line.split("(", 1)
            func_name = func_name.strip()
            args = [evaluate_expression(arg.strip(), context) for arg in arg_str.rstrip(")").split(",")]

            if func_name in functions:
                func_args, func_body = functions[func_name]
                if len(args) != len(func_args):
                    print(f"Error: {func_name} expected {len(func_args)} args, got {len(args)}")
                    return
                local_context = context.copy()
                for arg_name, val in zip(func_args, args):
                    local_context[arg_name] = val
                for line in func_body:
                    process_line([line], lines, index, local_context, env)
            else:
                print(f"Error: function '{func_name}' not defined")
        except Exception as e:
            print(f"Error calling function: {e}")

    elif stripped == "end":
        return

    else:
        try:
            exec('\n'.join(block), env)
        except Exception as e:
            print(f"Exec error: {e}")
