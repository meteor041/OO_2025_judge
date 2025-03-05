import os
import configparser

from plugin.find_java_files import find_java_files
from plugin.generate2 import generate_expression
from plugin.run_java_file2 import run_java_with_input_file_loop
from plugin.are_expression_equivalent2 import are_expressions_equivalent

def run2(config_file= 'config.ini', cmd=None):
    config = configparser.ConfigParser()
    config.read(config_file, encoding='utf-8')

    java_file_folder_path = config['DEFAULT']['java_file_folder_path']
    java_dir = config['DEFAULT']['java_dir']
    main_class = config['DEFAULT']['main_class']
    output_path = config['DEFAULT']['output_folder_path']

    # auto_generation = config['COMMAND']['auto_generation']
    # run_times = config['COMMAND']['run_times']
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
        input_lines = None
        for _ in range(times):
            if (input_lines == None):
                input_lines = [generate_expression(8) + "\n"]
            else:
                input_lines.append(generate_expression(8) + "\n")
        with open(input_file_path, "w") as f:
            for i, s in enumerate(input_lines):
                f.write(s)
    else:
        with open(input_file_path, "r") as f:
            input_lines = None
            new = ""
            para_length = 5
            count = 0
            for line in f:
                if count == 0:
                    para_length = 5 if line.strip() == '1' else 2
                new += line
                count += 1
                if count == para_length:
                    if input_lines == None:
                        input_lines = [new]
                    else:
                        input_lines.append(new)

    java_files = find_java_files(java_file_folder_path)
    output = run_java_with_input_file_loop(java_files, input_file_path, main_class, java_dir, output_path)
    output = [s.replace("^", "**") for s in output]

    for i, _output in enumerate(output):
        print(f"你的输出第{i+1}行: {_output}")

    print("input_lines length: " + str(len(input_lines)))
    # 是否出现错误
    all_right = True
    all_perfect = True
    for i, (_input, _output) in enumerate(zip(input_lines, output)):
        (res, score) = are_expressions_equivalent(_input, _output)
        print(f"第{i + 1}行结果: " + str(res) + " 分数： " + str(score))
        all_right = all_right and res
        all_perfect = all_perfect and (score == 1)

    print("是否全部运行正确:" + str(all_right))
    print("性能分是否满分:" + str(all_perfect))

    return all_right and all_perfect

if __name__ == "__main__":
    run2('config.ini', ['n',10])