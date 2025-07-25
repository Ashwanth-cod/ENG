def evaluate_expression(expr, context):
    expr = expr.replace("yes", "True").replace("no", "False")
    try:
        return eval(expr, {}, context)
    except Exception as e:
        print(f"Error evaluating '{expr}': {e}")
        return None
