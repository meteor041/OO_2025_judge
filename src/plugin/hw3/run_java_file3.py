import os
import subprocess


def getData(input_lines : list(str)) -> list(list(str)):
    # 3. 循环运行 Java 程序
    input_group = []
    i = 0
    run_times = 0
    while i < len(input_lines):
        line = input_lines[i]
        line = line.strip()  # 移除行尾的空白字符

        # 解析第一行，确定需要输入普通定义式的总行数
        try:
            num_lines = int(line)  # 第一行的数字
        except ValueError:
            print(f"第 {run_times + 1} 次运行: 第{i + 1}行不是有效的数字")
            continue

        # 根据第一行的数字，确定需要读取的行数
        if m == 0:
            total_lines = 1  # 包括第一行
        elif m == 1:
            total_lines = 2  # 包括第一行
        elif m == 2:
            total_lines = 3
        else:
            print(f"第 {run_times + 1} 次运行: 不支持的数字 {num_lines}")
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
        elif num_lines == 1:
            total_lines2 = 5  # 包括第一行
        else:
            print(f"第 {run_times + 1} 次运行: 不支持的数字 {num_lines}")
            continue

        # 读取后续行
        input_data.append(input_lines[i + 1])  # 第一行
        for _ in range(total_lines2 - 1):
            i += 1
            if i >= len(input_lines):
                print(f"第 {run_times + 1} 次运行: 输入行数不足")
                break
            input_data.append(input_lines[i].strip())
        input_group.append(input_data)
    return input_group


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
    output_path = os.path.join(output_path, "output.txt")

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
            input_lines = input_file.readlines().split('\n')
            outputs = []
            input_group = getData(input_lines)

        for run_times, input_data in enumerate(input_group):
            # 将多行输入拼接成一个字符串，用换行符分隔
            input_str = "\n".join(input_data)
            print('-' * 10 + f"第 {run_times+1} 次运行" + '-' * 10 + f"\n输入: {input_str}" )

            process = subprocess.Popen(  # 使用 Popen 来实时输入数据
                ["java", "-cp", java_dir, main_class],
                stdin=subprocess.PIPE,  # 使用管道作为标准输入
                stdout=subprocess.PIPE,  # 获取标准输出
                stderr=subprocess.PIPE,  # 获取标准错误
                text=True,
                cwd=java_dir
            )
            try:
                stdout, stderr = process.communicate(input=input_str, timeout=10) # 将数据写入管道

                if process.returncode != 0:
                    outputs.append(f"{stderr}".strip())
                    try:
                        mode = "w+" if run_times == 0 else "a"
                        with open(output_path, mode, encoding='utf-8') as f:  # 显式指定编码
                            f.write(f"第 {run_times+1} 次运行报错: {stderr.strip()}\n")
                    except Exception as e:
                        print(f"写入文件时发生错误: {e}")  # 打印错误信息
                else:
                    outputs.append(f"{stdout}".strip())
                    try:
                        mode = "w+" if run_times == 0 else "a"
                        with open(output_path, mode, encoding='utf-8') as f:  # 显式指定编码
                            f.write(f"第 {run_times+1} 次运行 : {stdout.strip()}\n")
                    except Exception as e:
                        print(f"写入文件时发生错误: {e}")  # 打印错误信息
            except subprocess.TimeoutExpired:
                outputs.append("subprocess.TimeoutExpired")
                print("java运行文件超时")

            run_times += 1
        return outputs  # 返回所有运行的输出

    except subprocess.CalledProcessError as e:
        return f"错误:\n{e.stderr}"
    except FileNotFoundError as e:
        return f"文件未找到错误:\n{e}"
    except Exception as e:
        return f"其他错误:\n{e}"