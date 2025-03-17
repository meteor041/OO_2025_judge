# 批量测试工具
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from plugin.hw3.generate3 import Generator
import configparser
from sympy import *
import subprocess
import random
import argparse
from datetime import datetime

x = symbols('x')
eps = 1e-6


def run3_single_cycle(jar_path, input_file, output_file):
    with open(output_file, "w") as outfile:
        result = subprocess.run(
            ["java", "-jar", jar_path],  # 运行 JAR 包的命令
            stdin=subprocess.PIPE,  # 重定向输入
            stdout=outfile,  # 重定向输出
            stderr=subprocess.PIPE,  # 捕获标准错误
            text=True  # 以文本模式处理输入输出
        )
        return result.stdout


def getData(input_file_path):
    with open(input_file_path, "r") as infile:
        input_lines = infile.readlines()
        input_group = []
        i = 0
        run_times = 0
        while i < len(input_lines):
            line = input_lines[i]
            line = line.strip()  # 移除行尾的空白字符

            # 解析第一行，确定需要输入普通定义式的总行数
            try:
                n = int(line)  # 第一行的数字
            except ValueError:
                print(f"第 {run_times + 1} 次运行: 第{i + 1}行不是有效的数字")
                return None

            # 根据第一行的数字，确定需要读取的行数
            if n == 0:
                total_lines = 1  # 包括第一行
            elif n == 1:
                total_lines = 2  # 包括第一行
            elif n == 2:
                total_lines = 3
            else:
                print(f"第 {run_times + 1} 次运行: 不支持的数字 {n}")
                continue

            # 读取后续行
            input_data = [line]  # 第一行
            for _ in range(total_lines - 1):
                i += 1
                if i >= len(input_lines):
                    print(f"第 {run_times + 1} 次运行: 输入行数不足")
                    break
                input_data.append(input_lines[i].strip())

            try:
                m = int(input_lines[i + 1])
            except ValueError:
                print(f"第 {run_times + 1} 次运行: 第{i + 1}行不是有效的数字")
                continue

            # 根据第一行的数字，确定需要读取的行数
            if m == 0:
                total_lines2 = 2  # 包括第一行
            elif m == 1:
                total_lines2 = 5  # 包括第一行
            else:
                print(f"第 {run_times + 1} 次运行: 不支持的数字 {n}")
                continue

            # 读取后续行
            # input_data.append(input_lines[i + 1])  # 第一行
            i += 1
            for _ in range(total_lines2):
                if i >= len(input_lines):
                    print(f"第 {run_times + 1} 次运行: 输入行数不足")
                    break
                input_data.append(input_lines[i].strip())
                i += 1
            input_group.append(input_data)
    return input_group


def run3(jar_file_path, input_file_path, output_file_path):
    input_group = getData(input_file_path)

    outputs = []
    # 打开输出文件
    with open(output_file_path, "w", encoding="utf-8") as outfile:
        for input_data in input_group:
            # 运行
            process = subprocess.Popen(
                ["java", "-jar", jar_file_path],  # 运行 JAR 包的命令
                stdin=subprocess.PIPE,  # 重定向输入
                stdout=subprocess.PIPE,  # 重定向输出
                stderr=subprocess.PIPE,  # 捕获标准错误
                text=True  # 以文本模式处理输入输出
            )
            # 发送输入数据
            process.stdin.write("\n".join(input_data) + "\n")
            process.stdin.close()

            # 读取输出
            output = process.stdout.readline().rstrip()
            outputs.append(output)
            outfile.write(output)  # 将输出写入文件
            process.wait()  # 等待进程结束
    return outputs


def run_jar(jar_file_path, input_data):
    try:
        # 运行 JAR 包
        process = subprocess.Popen(
            ["java", "-jar", jar_file_path],  # 运行 JAR 包的命令
            stdin=subprocess.PIPE,  # 重定向输入
            stdout=subprocess.PIPE,  # 重定向输出
            stderr=subprocess.PIPE,  # 捕获标准错误
            text=True  # 以文本模式处理输入输出
        )

        # 发送输入数据
        process.stdin.write("\n".join(input_data) + "\n")
        process.stdin.flush()

        # 读取输出和错误
        stdout, stderr = process.communicate(timeout=30)  # 等待进程结束并获取输出
        if stderr:
            print(f"Error: {stderr}")  # 打印错误信息
        return stdout.rstrip()  # 返回输出结果
    except subprocess.TimeoutExpired:
        print(f"Timeout: Process exceeded 30 seconds.")
        process.kill()  # 终止进程
        return None
    except Exception as e:
        print(f"Exception: {e}")
        return None


def run3_backup(jar_file_path, input_file_path, output_file_path, max_workers=4):
    # 获取输入数据
    input_group = getData(input_file_path)

    outputs = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # 提交任务
        futures = [executor.submit(run_jar, jar_file_path, input_data) for input_data in input_group]
        # 使用 map 方法保证顺序
        results = executor.map(lambda data: run_jar(jar_file_path, data), input_group)
        # 获取结果并写入文件
        with open(output_file_path, "w", encoding="utf-8") as outfile:
            for output in results:
                # output = future.result()
                if output:
                    outputs.append(output)
                    outfile.write(output + "\n")  # 将输出写入文件

    return outputs


def batchRun(jar_folder_path, jar_name_list, log_folder_path):
    '''
    遍历jar_file_path下的所有jar包,均对其运行run3,比较输出结果
    :param jar_folder_path:
    :param jar_name_list:
    :return:
    '''
    res = list()
    for i, name in enumerate(jar_name_list):
        jar_file_path = os.path.join(jar_folder_path, name + '.jar')
        input_file_path = os.path.join(log_folder_path, name, current_time, 'input.txt')
        if not os.path.exists(input_file_path):
            # 创建文件
            with open(input_file_path, "w") as f:
                f.write("")  # 写入空内容
        output_file_path = os.path.join(log_folder_path, name, current_time, 'output.txt')
        if not os.path.exists(output_file_path):
            # 创建文件
            with open(output_file_path, "w") as f:
                f.write("")  # 写入空内容
        print(f"第{i + 1}个测试对象:" + jar_file_path)
        with ThreadPoolExecutor() as executor:
            future = executor.submit(run3_backup, jar_file_path, input_file_path, output_file_path)
            try:
                res.append(future.result(timeout=60))
            except TimeoutError:
                future.cancel()
                res.append('timeout')

    print(f"---测试最终结果：{res}---".format(res=res))

    encounter_error_sentences = False

    num_columns = len(res[0]) if res else 0
    # 遍历每一行
    for col_idx in range(num_columns):
        evaluated_values = []
        # 生成一个随机值代入x
        random_value = random.uniform(-10, 10)
        for row in res:
            expr = row[col_idx] if col_idx < len(row) else None
            try:
                # 尝试将表达式转换为符号表达式并代入随机值
                evaluated_value = sympify(expr).subs(x, random_value)
                evaluated_values.append(evaluated_value)
            except (SympifyError, TypeError, AttributeError):
                # 如果转换失败，替换为114514，并设置标志变量为True
                evaluated_values.append(114514)
                encounter_error_sentences = True
        # 检查同一行的所有元素在代入x后的值是否相等
        if not encounter_error_sentences and all(abs(val - evaluated_values[0]) < eps for val in evaluated_values):
            print(f"Row {col_idx + 1}: All expressions are equal when x = {random_value}")
        else:
            print(f"Row {col_idx + 1}: Expressions are NOT  equal when x = {random_value}")
        print(["%.2f" % num for num in evaluated_values])


def read_from_jar_file(jar_folder_path: str) -> list[str]:
    # 获取所有以 .jar 结尾的文件
    return [f.strip(".jar") for f in os.listdir(jar_folder_path) if f.endswith(".jar")]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--auto', type=bool, default=False)
    parser.add_argument('--count', type=int, default=5)
    args = parser.parse_args()
    count = min(args.count, 10)
    auto_generate = args.auto
    config = configparser.ConfigParser()
    config.read("config.ini", encoding='utf-8')
    # 用户自定义输入所在文件
    input_file_path = config['BEAT']['input_file_path']
    # 测试用jar包所在文件
    jar_folder_path = config['BEAT']['jar_folder_path']
    # 输入输出结果所在文件夹
    log_folder_path = config['BEAT']['log_folder_path']
    jar_name_list = read_from_jar_file(jar_folder_path)
    if auto_generate:
        # 随机生成count条数据
        lines = ''
        for _ in range(count):
            lines += Generator(max_depth=2, max_length=200).generate_expression() + '\n'
    else:
        # 读取用户设置的输入
        with open(input_file_path, 'r') as f:
            lines = f.readlines()
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")  # 格式示例: 20231025_143022
    print("the program start at {}".format(current_time))
    for i in range(len(jar_name_list)):
        file_path = os.path.join(log_folder_path, jar_name_list[i], current_time, "input.txt")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.writelines(lines)

    batchRun(jar_folder_path, jar_name_list, log_folder_path)