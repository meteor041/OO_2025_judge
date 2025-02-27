from sympy import *
import subprocess
import os
import re
import configparser
import random

def generate_expression(max_depth=5):
    """
    随机生成包含x的表达式，遵循给定的语法规则。

    Args:
        max_depth: 最大递归深度，防止无限递归。

    Returns:
        一个字符串，表示生成的表达式。
    """

    def generate_whitespace():
        """生成空白项"""
        length = random.randint(0, 1)  # 空白字符的个数，可以调整
        return "".join(random.choice([" ", "\t"]) for _ in range(length))

    def generate_signed_integer():
        """生成带符号的整数"""
        sign = random.choice(["", "+", "-"])
        integer = generate_integer()
        return sign + integer

    def generate_integer(max_length=3):
        """生成允许前导零的整数"""
        length = random.randint(1, max_length)  # 整数的位数，可以调整
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
            return generate_signed_integer()  # 递归终止条件，返回一个简单的整数

        expression = ""
        if random.random() < 0.2:
            expression += generate_whitespace() + random.choice(["+", "-"]) + generate_whitespace()

        expression += generate_term(depth) + generate_whitespace()


        while random.random() < 0.4:
            expression += random.choice(["+", "-"]) + generate_whitespace() + generate_term(depth) + generate_whitespace()

        return expression

    return generate_expression_recursive(max_depth)

def run_java_with_input_file_loop(java_files, input_file_path, main_class, java_dir, output_path):
    """
    编译并运行 Java 文件，循环指定次数，每次从输入文件中读取一行作为输入。

    Args:
        java_files: Java 文件路径列表。
        input_file_path: 输入文件的路径。
        main_class: 主类的类名。
        java_dir: Java 文件所在的目录（用于编译和运行）。

    Returns:
        包含每次运行的输出的列表。如果编译失败或运行出错，返回错误信息。
    """
    output_path = output_path + "/result.txt"

    try:
        # 1. 编译 Java 文件
        compile_process = subprocess.run(
            ["javac"] + java_files,
            capture_output=True,
            text=True,
            check=True,
            cwd=java_dir
        )

        if compile_process.returncode != 0:
            return f"编译失败:\n{compile_process.stderr}"

        # 2. 读取输入文件行
        with open(input_file_path, "r") as input_file:
            input_lines = input_file.readlines()

        # 3. 循环运行 Java 程序
        outputs = []
        for i, line in enumerate(input_lines):
            line = line.strip()  # 移除行尾的空白字符
            print(f"第 {i+1} 次运行，输入: {line}")

            process = subprocess.Popen(  # 使用 Popen 来实时输入数据
                ["java", "-cp", java_dir, main_class],
                stdin=subprocess.PIPE,  # 使用管道作为标准输入
                stdout=subprocess.PIPE,  # 获取标准输出
                stderr=subprocess.PIPE,  # 获取标准错误
                text=True,
                cwd=java_dir
            )

            stdout, stderr = process.communicate(input=line) # 将数据写入管道
            #process.wait()

            if process.returncode != 0:
                outputs.append(f"{stderr}".strip())
                try:
                    mode = "w+" if i == 0 else "a"
                    with open(output_path, mode, encoding='utf-8') as f:  # 显式指定编码
                        f.write(f"运行失败 (第 {i+1} 次): {stderr}")
                except Exception as e:
                    print(f"写入文件时发生错误: {e}")  # 打印错误信息
            else:
                outputs.append(f"{stdout}".strip())
                try:
                    mode = "w+" if i == 0 else "a"
                    with open(output_path, mode, encoding='utf-8') as f:  # 显式指定编码
                        f.write(f"第 {i+1} 次运行输出: {stdout}")
                except Exception as e:
                    print(f"写入文件时发生错误: {e}")  # 打印错误信息

        return outputs  # 返回所有运行的输出

    except subprocess.CalledProcessError as e:
        return f"错误:\n{e.stderr}"
    except FileNotFoundError as e:
        return f"文件未找到错误:\n{e}"
    except Exception as e:
        return f"其他错误:\n{e}"

def find_java_files(directory):
    """
    递归地查找指定目录下所有以 .java 结尾的文件，并返回它们的绝对路径列表。

    Args:
        directory: 要搜索的根目录。

    Returns:
        一个包含所有找到的 .java 文件绝对路径的列表。
    """

    java_files = []
    for root, _, files in os.walk(directory):  # os.walk 递归地遍历目录树
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.abspath(os.path.join(root, file)))  # 构建绝对路径

    return java_files

def are_expressions_equivalent(expr1_str, expr2_str, x_value_count=10):
    """
    比较两个含 x 的表达式是否等价。

    Args:
        expr1_str: 第一个表达式的字符串表示形式 (例如: "x**2 + 2*x + 1").
        expr2_str: 第二个表达式的字符串表示形式 (例如: "(x + 1)**2").
        x_value_count: 用于数值比较的 x 值的数量 (默认: 10).

    Returns:
        bool: True 如果表达式等价, False 否则.
    """

    x = symbols('x')  # 定义符号变量

    try:
        # 删除前导零
        expr1_str = remove_leading_zeros_from_string(expr1_str)
        expr2_str = remove_leading_zeros_from_string(expr2_str)

        # 使用 sympy 尝试简化表达式并比较
        expr1 = expand(expr1_str)
        expr2 = expand(expr2_str)

        simplified_expr1 = simplify(expr1)
        simplified_expr2 = simplify(expr2)

        if simplified_expr1 != simplified_expr2:
            return False

        # 2. 数值比较 (如果 sympy 无法确定)
        for _ in range(x_value_count):
            x_val = random.uniform(-10, 10)  # 生成随机的 x 值
            if abs(expr1.subs(x, x_val) - expr2.subs(x, x_val)) > 1e-6:  # 允许一定的误差
                return False

        return True  # 数值比较也通过了

    except (SyntaxError, TypeError, ValueError) as e:
        print(f"表达式解析或计算时发生错误: {e}")
        return False  # 表达式无效

# 定义一个函数来消除数字中的前导零
def remove_leading_zeros_from_string(expr_str):
    # 使用正则表达式匹配所有数字并去掉前导零
    return re.sub(r'\b0+(\d+)', r'\1', expr_str)

def main():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')

    java_file_folder_path = config['DEFAULT']['java_file_folder_path']
    java_dir = config['DEFAULT']['java_dir']
    main_class = config['DEFAULT']['main_class']
    output_path = config['DEFAULT']['output_folder_path']
    input_file_path = output_path + "input.txt"

    times = input("输入运行次数：（最多100次,默认10次）")
    if times == '':
        times = 10
    else:
        times  = min(int(times), 100)
    input_lines = []
    for _ in range(times):
        input_lines.append(generate_expression(1) + "\n")
    with open(input_file_path, "w") as f:
        for s in input_lines:
            f.write(s)

    java_files = find_java_files(java_file_folder_path)
    output = run_java_with_input_file_loop(java_files, input_file_path, main_class, java_dir, output_path)
    output = [s.replace("^", "**") for s in output]

    for i, _output in enumerate(output):
        print(f"你的输出第{i+1}行: {_output}")

    input_lines = [s.replace("\t", " ") for s in input_lines]

    # 是否出现错误
    all_right = True

    for i, (_input, _output) in enumerate(zip(input_lines, output)):
        res = are_expressions_equivalent(_input, _output)
        print(f"第{i+1}行结果: " + str(res))
        all_right = all_right and res

    print("是否全部运行正确:" + str(all_right))

if __name__ == '__main__':
    main()
