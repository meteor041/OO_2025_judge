import random

from sympy.physics.vector.printing import params

class Generator:

    def __init__(self, max_depth, max_length):
        self.max_depth = max_depth
        self.max_length = max_length
        self.function_type = [random.randint(0, 3) for _ in range(3)]
        self.arguments = ['x']
        self.forbid_function = False
        
    def generate_expression(self) -> str:
        """随机生成函数调用的类型,0:无函数,1:f{n}(x),2:f{n}(y),3:f{n}(x,y)"""

        """
        随机生成包含x的表达式, 遵循给定的语法规则。
    
        Args:
            self.max_depth: 最大递归深度，防止无限递归。
    
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

        def generate_integer(integer_max_length=4):
            """生成允许前导零的整数"""
            length = random.randint(1, integer_max_length)  # 整数的位数，可以调整
            return "".join(random.choice("0123456789") for _ in range(length))

        def generate_exponent():
            """生成指数"""
            expression =  "^" + generate_whitespace()
            if random.random() < 0.5:
                expression += '+'
            expression += str(random.randint(0, 8))
            return expression

        def generate_power_function():
            """生成幂函数"""
            expression = random.choice(self.arguments)
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
            expression = random.choice(["sin", "cos"]) + generate_whitespace() + '(' + generate_whitespace()  + generate_factor(depth-1) + \
                          generate_whitespace() + ')'
            if rand < 0.5:
                generate_whitespace() + generate_exponent()
            return expression

        def generate_function_call(depth):
            if self.function_type[2] == 3:
                return "f{" + str(random.randint(0, 5)) + '}' + generate_whitespace() + '(' + generate_whitespace() + \
                    generate_factor(depth - 1) + ',' + generate_whitespace() + generate_factor(depth-1) + generate_whitespace() + ')'
            elif self.function_type[2] == 2 or self.function_type[2] == 1:
                return "f{" + str(random.randint(0, 5)) + '}' + generate_whitespace() + '(' + generate_whitespace() + \
                        generate_factor(depth - 1) + generate_whitespace() + ')'
            else:
                print("GENERATE_FUNCTION_CALL_ERROR!!!")

        def generate_variable_factor(depth):
            """生成变量因子"""
            rand = random.random()
            if rand < 0.3 and not self.forbid_function and self.function_type[2] != 0:
                return generate_function_call(depth)
            elif rand < 0.6:
                return generate_trigonometric_functions(depth)
            else:
                return generate_power_function()

        def generate_derivative_factor(depth):
            return 'dx' + generate_whitespace() + '(' + generate_whitespace() + generate_expression_factor(depth-1) + generate_whitespace() + ')'

        def generate_factor(depth):
            """生成因子"""
            rand = random.random()
            if rand < 0.3:
                return generate_variable_factor(depth)
            elif rand < 0.6:
                return generate_constant_factor()
            elif rand < 0.8:
                return generate_expression_factor(depth)
            else:
                return generate_derivative_factor(depth)

        def generate_term(depth):
            """生成项"""
            expression = ""
            if random.random() < 0.2:
                expression += random.choice(["+", "-"]) + generate_whitespace()

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

            expression = generate_whitespace()
            if random.random() < 0.2:
                expression +=  random.choice(["+", "-", ""]) + generate_whitespace()

            expression += generate_term(depth) + generate_whitespace()

            prob = 0.4
            while random.random() < prob :
                expression += random.choice(["+", "-"]) + generate_whitespace() + generate_term(depth) + generate_whitespace()
                prob *= 0.8
            return expression

        def generate_function_call_n_1(f_type):
            if f_type == 3:
                return 'f{n-1}' + generate_whitespace() + '(' + generate_factor(self.max_depth-1) + ',' + \
                    generate_whitespace() + generate_factor(self.max_depth-1) + generate_whitespace() +')'
            else:
                return 'f{n-1}' + generate_whitespace() + '(' + generate_factor(self.max_depth-1) \
                        + generate_whitespace() + ')'

        def generate_function_call_n_2(f_type):
            if f_type == 3:
                return 'f{n-2}' + generate_whitespace() + '(' + generate_factor(self.max_depth-1) + ',' + \
                    generate_whitespace() + generate_factor(self.max_depth-1) + generate_whitespace() +')'
            else:
                return 'f{n-2}' + generate_whitespace() + '(' + generate_factor(self.max_depth-1) \
                        + generate_whitespace() + ')'

        def generate_function_definition(self):
            self.arguments = ['x', 'y'] if self.function_type[2] == 3 else ['x'] if self.function_type[2] == 1 else ['y']
            value = 'x' if self.function_type[2] == 1 else 'y' if self.function_type[2] == 2 else\
                                    'x' + generate_whitespace() + ',' + generate_whitespace() + 'y' if self.function_type[2] == 3 \
                                    else 'y' + generate_whitespace() + ',' + generate_whitespace() + 'x'
            self.forbid_function = True
            initial_definition0 = 'f{0}' + generate_whitespace() + '(' + generate_whitespace() + value +\
                                 generate_whitespace() + ')' + generate_whitespace() + '=' + generate_whitespace() +\
                generate_expression_recursive(self.max_depth)
            while len(initial_definition0) > 75:
                initial_definition0 = 'f{0}' + generate_whitespace() + '(' + generate_whitespace() + value + \
                                      generate_whitespace() + ')' + generate_whitespace() + '=' + generate_whitespace() + \
                                      generate_expression_recursive(self.max_depth)
            initial_definition1 = 'f{1}' + generate_whitespace() + '(' + generate_whitespace() + value + \
                                  generate_whitespace() + ')' + generate_whitespace() + '=' + generate_whitespace() + \
                                  generate_expression_recursive(self.max_depth)
            while len(initial_definition1) > 75:
                initial_definition1 = 'f{1}' + generate_whitespace() + '(' + generate_whitespace() + value + \
                                      generate_whitespace() + ')' + generate_whitespace() + '=' + generate_whitespace() + \
                                      generate_expression_recursive(self.max_depth)
            initial_definition = 'f{n}' + generate_whitespace() + '(' + generate_whitespace() + value + \
                                  generate_whitespace() + ')' + generate_whitespace() + '=' + \
                                  generate_constant_factor() + generate_whitespace() + '*' + generate_whitespace() + \
                                  generate_function_call_n_1(self.function_type[2]) + generate_whitespace() + random.choice(['+', '-']) + \
                                  generate_constant_factor() + generate_whitespace() + '*' + generate_function_call_n_2(self.function_type[2]) + \
                                  '+' + generate_expression_recursive(self.max_depth)
            while len(initial_definition) > 75:
                initial_definition = 'f{n}' + generate_whitespace() + '(' + generate_whitespace() + value +\
                                      generate_whitespace() + ')' + generate_whitespace() + '=' + \
                                      generate_constant_factor() + generate_whitespace() + '*' + generate_whitespace() + \
                                      generate_function_call_n_1(self.function_type[2]) + generate_whitespace() + random.choice(['+', '-']) + \
                                      generate_constant_factor() + generate_whitespace() + '*' + generate_function_call_n_2(self.function_type[2]) + \
                                      '+' + generate_expression_recursive(self.max_depth)
            self.arguments = ['x']
            self.forbid_function = False
            definition_list = [initial_definition0, initial_definition1, initial_definition]
            random.shuffle(definition_list)
            return definition_list[0] + '\n' + definition_list[1] + '\n' + definition_list[2]

        def generate_self_definition(type : str, mode : int) -> str:
            var = 'x' if mode == 1 else 'y' if mode == 2 else 'x,y' if mode == 3 else 'y,x'
            if mode == 3 or mode == 4:
                self.arguments = ['x', 'y']
                s = type + '(' + var + ')' + '=' + generate_expression_recursive(self.max_depth)
                self.arguments = ['x']
            else:
                s = type + '(' + var + ')' + '=' + generate_expression_recursive(self.max_depth)
            return s

        s = generate_expression_recursive(self.max_depth) + '\n'
        while len(s) > self.max_length:
            s = generate_expression_recursive(self.max_depth) + '\n'
        def0 = str(min(self.function_type[0], 1) + min(self.function_type[1], 1)) + '\n'
        if self.function_type[0] != 0:
            def1 = generate_self_definition("g", self.function_type[0]) + '\n'
            while len(def1) > 50:
                def1 = generate_self_definition("g", self.function_type[0]) + '\n'
        else:
            def1 = ''
        if self.function_type[1] != 0:
            def2 = generate_self_definition("h", self.function_type[1]) + '\n'
            while len(def2) > 50:
                def2 = generate_self_definition("h", self.function_type[1]) + '\n'
        else:
            def2 = ''
        if self.function_type[2] == 0:
            recur =  '0\n'
        else:
            recur = '1\n' +  generate_function_definition(self)
        return def0  + def1  + def2 + recur + s


if __name__ == '__main__':
    res = Generator(8, 200).generate_expression()
    print(res)