from sympy import *
import random
import re
from concurrent.futures import ThreadPoolExecutor, TimeoutError

from ..public.remove_leading_zero import remove_leading_zeros_from_string
from ..hw2.spreader2 import expand_expression
from ..public.ai_expression import ai_test_equivalent


def are_expressions_equivalent(expr1_str : list[str], expr2_str : str, ai_enable=False, api=None, x_value_count=10):
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
    y = symbols('y')

    # try:
    expr1_list = expr1_str.split('\n') # 列表

    n = int(expr1_list[0])
    if n == 1:
        # 正则表达式匹配 f{数字或n}(参数)=表达式
        pattern = re.compile(r'^f\{(\d+|n)}\((?:.+)\)=.+$')
        str0 = None
        str1 = None
        recursion_str = None
        for s in expr1_list[1:4]:
            # 去除空白字符确保匹配准确
            cleaned = s.replace(" ", "").replace("\t", "").replace("\n", "")
            match = pattern.match(cleaned)
            if not match:
                raise ValueError(f"无效的定义格式: {s}")

            key = match.group(1)
            if key == '0':
                if str0 is not None:
                    raise ValueError("检测到多个 f{0} 定义")
                str0 = cleaned
            elif key == '1':
                if str1 is not None:
                    raise ValueError("检测到多个 f{1} 定义")
                str1 = cleaned
            elif key == 'n':
                if recursion_str is not None:
                    raise ValueError("检测到多个 f{n} 定义")
                recursion_str = cleaned
            else:
                raise ValueError(f"未知的定义标识符: f{{{key}}}")
        expr1_str = expr1_list[4].replace(" ", "").replace("\t", "").replace("\n", "")

        # 展开式子,消去所有的递推式
        expr1_str = expand_expression(s = expr1_str, recursion_str = recursion_str, str0 = str0, str1 = str1)

    else:
        expr1_str = expr1_list[1]
    # expr1_str = expand_expression("")

    # 删除前导零
    expr1 = remove_leading_zeros_from_string(expr1_str).replace("^", "**")
    expr2 = remove_leading_zeros_from_string(expr2_str).replace("^", "**")

    expr1 = parse_expr(expr1)
    expr2 = parse_expr(expr2)

    if ai_enable == True:
        return ai_test_equivalent(expr1, expr2, api) == 0

    # # 2. 数值比较 (如果 sympy 无法确定)
    res = True
    min_diff = float('inf')
    for _ in range(x_value_count):
        x_val = random.uniform(-10, 10)  # 生成随机的 x 值
        diff = abs(expr1.subs(x, x_val) - expr2.subs(x, x_val)).evalf()
        min_diff = min(min_diff, diff)
        if  diff > 1e-6:  # 允许一定的误差
            res = False

    if not res:
        try:
            # 使用 ThreadPoolExecutor 设置超时
            with ThreadPoolExecutor() as executor:
                future = executor.submit(expr1.equals, expr2)
                res = future.result(timeout=3)  # 设置超时时间为 3 秒
        except TimeoutError:
            # 如果超时，返回数值代入比较的结果
            print("equals 方法超时，返回值最小计算结果为: " + str(min_diff))
            return False

    return True

    # except (SyntaxError, TypeError, ValueError) as e:
    #     print(f"(are_expression_equivalent2)表达式解析或计算时发生错误: {e}")
    #     return False, -1  # 表达式无效