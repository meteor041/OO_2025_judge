import os


def find_main_java_files(folder_path):
    """
    查找指定文件夹中包含 `public static void main(String[] args)` 的 Java 文件。

    :param folder_path: 要搜索的文件夹路径
    :return: 包含主函数的 Java 文件路径列表
    """
    main_java_files_list = []

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件是否为 Java 文件
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                try:
                    # 打开文件并检查内容
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                        # 检查是否包含主函数
                        if "public static void main(String[] args)" in content:
                            main_java_files_list.append(file)
                except Exception as e:
                    print(f"无法读取文件 {file_path}: {e}")
    if len(main_java_files_list) == 1:
        return main_java_files_list[0].rstrip(".java")
    elif len(main_java_files_list) == 0:
        print("未找到主类文件")
        raise FileNotFoundError
    else:
        print("文件夹中含有多个主类文件")
        return main_java_files_list[0].rstrip(".java")


if __name__ == "__main__":
    # 指定要搜索的文件夹路径
    folder_path = "C:\\Users\\Liu Xinyu\\PycharmProjects\\OO_hw1_judge\\HW2CODE\\天权星\\src"

    # 查找包含主函数的 Java 文件
    main_java_files = find_main_java_files(folder_path)

    # 输出结果
    print(main_java_files)