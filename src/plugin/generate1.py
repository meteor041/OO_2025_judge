import random
def generate_expression(max_depth=8):
    """
    随机生成包含x的表达式, 遵循给定的语法规则。

    Args:
        max_depth: 最大递归深度，防止无限递归。

    Returns:
        一个字符串，表示生成的表达式。
    """

    def generate_whitespace():
        """生成空白项"""
        length = random.randint(0, 2)  # 空白字符的个数，可以调整
        return "".join(random.choice([" ", "\t"]) for _ in range(length))

    def generate_signed_integer():
        """生成带符号的整数"""
        sign = random.choice(["", "+", "-"])
        integer = generate_integer()
        return sign + integer

    def generate_integer(maxLength=4):
        """生成允许前导零的整数"""
        length = random.randint(1, maxLength)  # 整数的位数，可以调整
        return "".join(random.choice("0123456789") for _ in range(length))

    def generate_exponent():
        """生成指数"""
        return "^" + generate_whitespace() + generate_integer(1)

    def generate_power_function():
        """生成幂函数"""
        expression = "x"
        if random.random() < 0.3:  # 30%的概率生成指数
            expression += generate_whitespace() + generate_exponent()
        return expression

    def generate_constant_factor():
        """生成常数因子"""
        return generate_signed_integer()

    def generate_expression_factor(depth):
        """生成表达式因子"""
        expression = "(" + generate_expression_recursive(depth - 1) + ")"
        if random.random() < 0.3:  # 30%的概率生成指数
            expression += generate_whitespace() + generate_exponent()
        return expression

    def generate_variable_factor():
        """生成变量因子"""
        return generate_power_function()

    def generate_factor(depth):
        """生成因子"""
        rand = random.random()
        if rand < 0.3:
            return generate_variable_factor()
        elif rand < 0.6:
            return generate_constant_factor()
        else:
            return generate_expression_factor(depth)

    def generate_term(depth):
        """生成项"""
        expression = ""
        if random.random() < 0.2:
            expression += random.choice(["+", "-"]) + generate_whitespace()

        expression += generate_factor(depth)

        while random.random() < 0.3:
            expression += generate_whitespace() + "*" + generate_whitespace() + generate_factor(depth)

        return expression


    def generate_expression_recursive(depth):
        """递归生成表达式"""
        if depth <= 0:
            if random.random() < 0.5:
                return generate_signed_integer()  # 递归终止条件，返回一个简单的整数
            else:
                return generate_variable_factor()

        expression = ""
        if random.random() < 0.2:
            expression += generate_whitespace() + random.choice(["+", "-"]) + generate_whitespace()

        expression += generate_term(depth) + generate_whitespace()


        while random.random() < 0.4:
            expression += random.choice(["+", "-"]) + generate_whitespace() + generate_term(depth) + generate_whitespace()

        return expression

    return generate_expression_recursive(max_depth)
