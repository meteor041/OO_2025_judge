import os
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