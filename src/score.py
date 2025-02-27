def score_expr(std, expr):
    expr_str = str(expr).strip().replace(" ", "").replace("\t", "").replace("**", "^")
    std_str = str(std).strip().replace(" ", "").replace("\t", "").replace("**", "^")
    x = len(expr_str) / len(std_str)
    if x <= 1:
        r = 1
    elif x <= 1.5:
        r = (-31.8239 * x ** 4 + 155.9038 * x ** 3
             - 279.2180 * x ** 2+214.0743 * x - 57.93700)
    else:
        r = 0

    return r