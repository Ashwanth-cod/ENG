def evaluate_expression(expr, context):
    # Replace variables in context into the expression
    safe_context = {**context, "str": str, "int": int, "float": float}

    try:
        return eval(expr, {"__builtins__": {}}, safe_context)
    except Exception as e:
        return f"Error: {e}"
