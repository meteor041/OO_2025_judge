from sympy import *
import subprocess
import os

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
    output_path = output_path + "\\result.txt"

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
                        f.write(f"运行失败 (第 {i+1} 次):\n{stderr}")
                except Exception as e:
                    print(f"写入文件时发生错误: {e}")  # 打印错误信息
            else:
                outputs.append(f"{stdout}".strip())
                try:
                    mode = "w+" if i == 0 else "a"
                    with open(output_path, mode, encoding='utf-8') as f:  # 显式指定编码
                        f.write(f"第 {i+1} 次运行输出:\n{stdout}")
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
        # 1. 使用 sympy 尝试简化表达式并比较
        expr1 = sympify(expr1_str)
        expr2 = sympify(expr2_str)

        simplified_expr1 = simplify(expr1)
        simplified_expr2 = simplify(expr2)

        if simplified_expr1 == simplified_expr2:
            return True

        # 2. 数值比较 (如果 sympy 无法确定)
        import random
        for _ in range(x_value_count):
            x_val = random.uniform(-10, 10)  # 生成随机的 x 值
            if abs(expr1.subs(x, x_val) - expr2.subs(x, x_val)) > 1e-6:  # 允许一定的误差
                return False

        return True  # 数值比较也通过了

    except (SyntaxError, TypeError, ValueError) as e:
        print(f"表达式解析或计算时发生错误: {e}")
        return False  # 表达式无效


java_file_folder_path = ["C:\\Users\\Liu Xinyu\\IdeaProjects\\oo_homework_2025_23371510_hw_1\\src",
                         "C:\\Users\\Liu Xinyu\\IdeaProjects\\oo_homework_2025_23371510_hw_1\\src\\node"]
java_files = find_java_files(java_file_folder_path[0]) + find_java_files(java_file_folder_path[1])
print(java_files)
input_file_path = "C:\\Users\\Liu Xinyu\\IdeaProjects\\oo_homework_2025_23371510_hw_1\\test\\file.txt"
java_dir = "C:\\Users\\Liu Xinyu\\IdeaProjects\\oo_homework_2025_23371510_hw_1\\src"
main_class = "MainClass"

output_path = "C:\\Users\\Liu Xinyu\\PycharmProjects\\OO_hw1_judge\\log"
output = run_java_with_input_file_loop(java_files, input_file_path, main_class, java_dir, output_path)
output = [s.replace("^", "**") for s in output]
for _output in output:
    print(_output)

with open(input_file_path, "r") as f:
    input_lines = f.readlines()

for i, (_input, _output) in enumerate(zip(input_lines, output)):
    print(f"line {i+1}: " + str(are_expressions_equivalent(_input, _output)))