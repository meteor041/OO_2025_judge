from src.plugin.score import score_expr
from sympy import *
import random

from src.plugin.remove_leading_zero import remove_leading_zeros_from_string

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
        # 删除前导零
        expr1_str = remove_leading_zeros_from_string(expr1_str)
        expr2_str = remove_leading_zeros_from_string(expr2_str)

        # 使用 sympy 尝试简化表达式并比较
        expr1 = expand(expr1_str)
        expr2 = expand(expr2_str)

        simplified_expr1 = simplify(expr1)
        simplified_expr2 = simplify(expr2)

        if simplified_expr1 != simplified_expr2:
            return False, -1

        score = score_expr(simplified_expr1, expr2_str)

        # 2. 数值比较 (如果 sympy 无法确定)
        for _ in range(x_value_count):
            x_val = random.uniform(-10, 10)  # 生成随机的 x 值
            if abs(expr1.subs(x, x_val) - expr2.subs(x, x_val)) > 1e-6:  # 允许一定的误差
                return False, -1

        return True, score  # 数值比较也通过了

    except (SyntaxError, TypeError, ValueError) as e:
        print(f"表达式解析或计算时发生错误: {e}")
        return False, -1  # 表达式无效