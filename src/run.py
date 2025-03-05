import os
import configparser

from src.plugin.hw1.are_expression_equivalent1 import are_expressions_equivalent
from src.plugin.public.find_java_files import find_java_files
from src.plugin.hw1.run_java_file1 import run_java_with_input_file_loop
from src.plugin.hw1.generate1 import generate_expression
# def disable_print(*args, **kwargs):
#     pass
#
#
# # 替换 print
# print = disable_print

def run(config_file='config.ini', cmd=None):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    java_file_folder_path = config['DEFAULT']['java_file_folder_path']
    java_dir = config['DEFAULT']['java_dir']
    main_class = config['DEFAULT']['main_class']
    output_path = config['DEFAULT']['output_folder_path']
    input_file_path = os.path.join(output_path, "input.txt")
    if not os.path.exists(os.path.dirname(input_file_path)):
        os.mkdir(os.path.dirname(input_file_path))
        print(str(os.path.basename(input_file_path)) + "已创建")
    useGen = input("是否使用内置数据生成(y/n): ") if cmd == None else cmd[0]
    if useGen.lower() == 'y' or useGen == '':
        times = input("输入运行次数: (最多1000次,默认10次): ") if cmd == None else cmd[1]
        if times == '':
            times = 10
        else:
            times = min(int(times), 1000)
        input_lines = []
        for _ in range(times):
            input_lines.append(generate_expression(1) + "\n")
        with open(input_file_path, "w") as f:
            for i, s in enumerate(input_lines):
                f.write(s)
    else:
        with open(input_file_path, "r") as f:
            input_lines = f.readlines()

    java_files = find_java_files(java_file_folder_path)
    output = run_java_with_input_file_loop(java_files, input_file_path, main_class, java_dir, output_path)
    output = [s.replace("^", "**") for s in output]

    for i, _output in enumerate(output):
        print(f"你的输出第{i+1}行: {_output}")

    input_lines = [s.replace("\t", " ") for s in input_lines]

    # 是否出现错误
    all_right = True
    all_perfect = True
    for i, (_input, _output) in enumerate(zip(input_lines, output)):
        if '(' in _output or ')' in _output:
            res, score = False, -1
        else:
            (res, score) = are_expressions_equivalent(_input, _output)
        print(f"第{i+1}行结果: " + str(res) + " 分数： " + str(score))
        all_right = all_right and res
        all_perfect = all_perfect and (score == 1)

    print("是否全部运行正确:" + str(all_right))
    print("性能分是否满分:" + str(all_perfect))

    return all_right and all_perfect

if __name__ == '__main__':
    run("config.ini")
