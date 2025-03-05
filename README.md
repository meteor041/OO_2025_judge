# OO2025作业测试程序

## 项目简介

项目简介
本项目旨在为 OO2025 课程的学生提供一个自动化测试工具，用于测试 `Java` 作业的正确性。通过配置 `config.ini` 文件，程序可以自动运行指定的 `Java` 文件，并生成测试样例和输出结果。

## 项目结构

## 步骤

1. 填充`config.ini`文件

在运行测试程序之前，需要先配置 `config.ini` 文件。该文件包含以下配置项：
```ini
java_file_folder_path : Java文件存储的文件夹(绝对位置)
java_dir : 主类文件所在目录位置(绝对位置)
main_class : 主类名称(示例:MainClass)
output_folder_path : Java文件运行输出结果(`output.txt`)和自动生成测试样例文本(`input.txt`)所在文件夹位置(绝对位置)
```
 
示例 `config.ini` 文件内容:

```ini
[java]
java_file_folder_path = /path/to/your/java/files
java_dir = /path/to/your/main/class/directory
main_class = MainClass
output_folder_path = /path/to/output/folder
```
2. 运行作业测试程序
   1.  运行第一周作业测试程序

        要运行第一周作业的测试程序，请执行以下命令：
        
          ``` bash
        cd src
        python run.py
          ```

   2. 运行第二周作业测试程序

        要运行第二周作业的测试程序，请执行以下命令：

        ``` bash
        cd src
        python run.py
        ```
      
3. 查看输出结果

程序运行后，输出结果将保存在 `output_folder_path` 指定的文件夹中。你将看到以下文件：

- `input.txt`: 自动生成的测试样例。

- `output.txt`: `Java` 程序运行的结果。

## 注意事项

- 确保 `config.ini` 文件中的路径配置正确，特别是绝对路径的准确性。

- 确保 `Java` 环境已正确安装，并且可以在命令行中运行 `java` 和 `javac` 命令。

- 如果 `Java` 文件有依赖库，请确保这些库已正确配置在 `CLASSPATH` 中

## 常见问题

   1. 程序无法找到 `Java` 文件
   
   - 检查 `java_file_folder_path` 和 `java_dir` 配置是否正确。
   
   - 确保 `Java` 文件路径没有拼写错误。

   2. 程序无法运行主类
   
   - 检查 `main_class` 配置是否正确。

   - 确保主类文件已编译，并且可以在指定目录中找到。

   3. 输出文件为空
   
   - 检查 `Java` 程序是否有输出到标准输出（`System.out`）。
   
   - 确保测试样例 `input.txt` 已正确生成。

## 贡献

如果你有任何改进建议或发现问题，欢迎提交 `Issue` 或 `Pull Request`。

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](https://github.com/meteor041/OO_2025_judge/blob/main/LICENSE) 文件。
