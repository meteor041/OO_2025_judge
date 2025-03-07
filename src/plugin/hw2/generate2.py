import random

from sympy.physics.vector.printing import params


function_type = random.randint(0, 3)
arguments = ['x']
tmp = 0
forbid_function = False
def generate_expression(max_depth=8, max_length=200) -> str:
    """随机生成函数调用的类型,0:无函数,1:f{n}(x),2:f{n}(y),3:f{n}(x,y)"""

    """
    随机生成包含x的表达式, 遵循给定的语法规则。

    Args:
        max_depth: 最大递归深度，防止无限递归。

    Returns:
        一个字符串，表示生成的表达式。
    """
    global function_type
    global arguments
    global tmp
    global forbid_function
    function_type  = random.randint(0, 3)
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
        return "^" + generate_whitespace() + str(random.randint(0, 8))

    def generate_power_function():
        """生成幂函数"""
        expression = random.choice(arguments)
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

    def generate_trigonometric_functions(depth):
        """生成三角函数"""
        rand = random.random()
        expression = random.choice(["sin", "cos"]) + generate_whitespace() + '(' + generate_factor(depth-1) + \
                      generate_whitespace() + ')' + generate_whitespace() + generate_exponent()
        return expression

    def generate_function_call(depth):
        global function_type
        if function_type == 3:
            return "f{" + str(random.randint(0, 5)) + '}' + generate_whitespace() + '(' + generate_whitespace() + \
                generate_factor(depth - 1) + ',' + generate_whitespace() + generate_factor(depth-1) + generate_whitespace() + ')'
        elif function_type == 2 or function_type == 1:
            return "f{" + str(random.randint(0, 5)) + '}' + generate_whitespace() + '(' + generate_whitespace() + \
                    generate_factor(depth - 1) + ')'
        else:
            print("GENERATE_FUNCTION_CALL_ERROR!!!")

    def generate_variable_factor(depth):
        """生成变量因子"""
        global function_type
        global forbid_function
        rand = random.random()
        if rand < 0.3 and not forbid_function and function_type != 0:
            return generate_function_call(depth)
        elif rand < 0.6:
            return generate_trigonometric_functions(depth)
        else:
            return generate_power_function()

    def generate_factor(depth):
        """生成因子"""
        rand = random.random()
        if rand < 0.3:
            return generate_variable_factor(depth)
        elif rand < 0.6:
            return generate_constant_factor()
        else:
            return generate_expression_factor(depth)

    def generate_term(depth):
        """生成项"""
        expression = ""
        if random.random() < 0.2:
            expression += random.choice(["+", "-", ""]) + generate_whitespace()

        expression += generate_factor(depth)

        prob = 0.3
        while random.random() < prob:
            expression += generate_whitespace() + "*" + generate_whitespace() + generate_factor(depth)
            prob *= 0.5
        return expression


    def generate_expression_recursive(depth):
        """递归生成表达式"""
        if depth <= 0:
            if random.random() < 0.5:
                return generate_signed_integer()  # 递归终止条件，返回一个简单的整数
            else:
                return generate_power_function()

        expression = ""
        if random.random() < 0.2:
            expression += generate_whitespace() + random.choice(["+", "-", ""]) + generate_whitespace()

        expression += generate_term(depth) + generate_whitespace()

        prob = 0.4
        while random.random() < prob :
            expression += random.choice(["+", "-"]) + generate_whitespace() + generate_term(depth) + generate_whitespace()
            prob *= 0.8
        return expression

    def generate_function_call_n_1(f_type):
        if f_type == 3:
            return 'f{n-1}' + generate_whitespace() + '(' + generate_factor(max_depth-1) + ',' + \
                generate_whitespace() + generate_factor(max_depth-1) + generate_whitespace() +')'
        else:
            return 'f{n-1}' + generate_whitespace() + '(' + generate_expression_recursive(max_depth-1) \
                    + generate_whitespace() + ')'

    def generate_function_call_n_2(f_type):
        if f_type == 3:
            return 'f{n-2}' + generate_whitespace() + '(' + generate_factor(max_depth-1) + ',' + \
                generate_whitespace() + generate_factor(max_depth-1) + generate_whitespace() +')'
        else:
            return 'f{n-2}' + generate_whitespace() + '(' + generate_expression_recursive(max_depth-1) \
                    + generate_whitespace() + ')'

    def generate_function_definition():
        global function_type
        global arguments
        global tmp
        global forbid_function
        arguments = ['x', 'y'] if function_type == 3 else ['x'] if function_type == 1 else ['y']
        value = 'x' if function_type == 1 else 'y' if function_type == 2 else 'x' + \
                                generate_whitespace() + ',' + generate_whitespace() + 'y'
        forbid_function = True
        initial_definition0 = 'f{0}' + generate_whitespace() + '(' + generate_whitespace() + value +\
                             generate_whitespace() + ')' + generate_whitespace() + '=' + generate_whitespace() +\
            generate_expression_recursive(max_depth)
        while len(initial_definition0) > 75:
            initial_definition0 = 'f{0}' + generate_whitespace() + '(' + generate_whitespace() + value + \
                                  generate_whitespace() + ')' + generate_whitespace() + '=' + generate_whitespace() + \
                                  generate_expression_recursive(max_depth)
        initial_definition1 = 'f{1}' + generate_whitespace() + '(' + generate_whitespace() + value + \
                              generate_whitespace() + ')' + generate_whitespace() + '=' + generate_whitespace() + \
                              generate_expression_recursive(max_depth)
        while len(initial_definition1) > 75:
            initial_definition1 = 'f{1}' + generate_whitespace() + '(' + generate_whitespace() + value + \
                                  generate_whitespace() + ')' + generate_whitespace() + '=' + generate_whitespace() + \
                                  generate_expression_recursive(max_depth)
        initial_definition = 'f{n}' + generate_whitespace() + '(' + generate_whitespace() + value + \
                              generate_whitespace() + ')' + generate_whitespace() + '=' + \
                              generate_constant_factor() + generate_whitespace() + '*' + generate_whitespace() + \
                              generate_function_call_n_1(function_type) + generate_whitespace() + random.choice(['+', '-']) + \
                              generate_constant_factor() + generate_whitespace() + '*' + generate_function_call_n_2(function_type) + \
                              random.choice(['+', '-']) + generate_expression_recursive(max_depth)
        while len(initial_definition) > 75:
            initial_definition = 'f{n}' + generate_whitespace() + '(' + generate_whitespace() + value +\
                                  generate_whitespace() + ')' + generate_whitespace() + '=' + \
                                  generate_constant_factor() + generate_whitespace() + '*' + generate_whitespace() + \
                                  generate_function_call_n_1(function_type) + generate_whitespace() + random.choice(['+', '-']) + \
                                  generate_constant_factor() + generate_whitespace() + '*' + generate_function_call_n_2(function_type) + \
                                  random.choice(['+', '-']) + generate_expression_recursive(max_depth)
        arguments = ['x']
        forbid_function = False
        definition_list = [initial_definition0, initial_definition1, initial_definition]
        random.shuffle(definition_list)
        return definition_list[0] + '\n' + definition_list[1] + '\n' + definition_list[2]

    s = generate_expression_recursive(max_depth)
    while len(s) > max_length:
        s = generate_expression_recursive(max_depth)
    if function_type == 0:
        return '0\n' + s
    else:
        return '1\n' +  generate_function_definition() + '\n' + s


if __name__ == '__main__':
    res = generate_expression(max_depth=1)
    print(res)