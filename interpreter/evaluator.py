def evaluate_expression(expr, context):
    allowed_builtins = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "len": len,
        "abs": abs,
        "max": max,
        "min": min,
        "list": list,
        "dict": dict,
        "range": range,
    }

    return eval(expr, {"__builtins__": allowed_builtins}, context)
