# 定义一个函数来消除数字中的前导零
import re

def remove_leading_zeros_from_string(expr_str):
    # 使用正则表达式匹配所有数字并去掉前导零
    return re.sub(r'\b0+(\d+)', r'\1', expr_str).replace(" ", "").replace("\t", "")