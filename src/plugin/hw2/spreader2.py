import re

class Spreader:
    definitions_list = [None] * 3  # 用于存储 f{0}, f{1}, f{n} 的表达式
    flag = 0  # 用于标记函数的参数类型

    @staticmethod
    def set_definition(definitions):
        """
        解析并存储定义
        :param definitions: 包含 f{0}, f{1}, f{n} 定义的列表
        """
        # 正则表达式匹配 f{常数|n}(...)=表达式
        pattern = re.compile(r"^f\{(\d+|n)}\((.+)\)=(.+)$")

        for s in definitions:
            s = s.replace("\n", "").replace("\t", "").replace(" ", "")
            matcher = pattern.match(s)
            if matcher:
                params = matcher.group(2)
                if params == "x":
                    Spreader.flag = 1
                elif params == "y":
                    Spreader.flag = 2
                elif params == "x,y":
                    Spreader.flag = 3
                else:
                    raise ValueError(f"Unknown definition: {s}")

                key = matcher.group(1)
                if key == "0":
                    Spreader.definitions_list[0] = matcher.group(3)
                elif key == "1":
                    Spreader.definitions_list[1] = matcher.group(3)
                elif key == "n":
                    Spreader.definitions_list[2] = matcher.group(3)
                else:
                    print(f"Unknown definition: {s}")
            else:
                raise ValueError(f"Unknown definition: {s}")

    @staticmethod
    def spread(input_str):
        """
        展开输入字符串中的函数调用
        :param input_str: 输入字符串
        :return: 展开后的字符串
        """
        input_str = input_str.replace(" ", "").replace("\t", "").replace("\n", "")
        pattern = re.compile(r"f\{(\d+)}\(")
        matcher = pattern.search(input_str)

        while matcher:
            ns = matcher.group(1)  # f{n} 中的 n
            param1_builder = []
            param2_builder = []
            param1 = None
            param2 = None

            count = 1
            pos = matcher.end()

            # 根据 flag 处理参数
            if Spreader.flag == 1:
                # 含 x 参数
                while pos < len(input_str):
                    c = input_str[pos]
                    if c == '(':
                        count += 1
                    elif c == ')':
                        count -= 1
                    if count == 0:
                        break
                    param1_builder.append(c)
                    pos += 1
                param1 = ''.join(param1_builder)
            elif Spreader.flag == 2:
                # 含 y 参数
                while pos < len(input_str):
                    c = input_str[pos]
                    if c == '(':
                        count += 1
                    elif c == ')':
                        count -= 1
                    if count == 0:
                        break
                    param2_builder.append(c)
                    pos += 1
                param2 = ''.join(param2_builder)
            elif Spreader.flag == 3:
                # 含 x, y 参数
                while pos < len(input_str):
                    c = input_str[pos]
                    if c == ',' and count == 1:
                        pos += 1
                        break
                    if c == '(':
                        count += 1
                    elif c == ')':
                        count -= 1
                    if count == 0:
                        break
                    param1_builder.append(c)
                    pos += 1
                while pos < len(input_str):
                    c = input_str[pos]
                    if c == '(':
                        count += 1
                    elif c == ')':
                        count -= 1
                    if count == 0:
                        break
                    param2_builder.append(c)
                    pos += 1
                param1 = ''.join(param1_builder)
                param2 = ''.join(param2_builder)
            else:
                raise ValueError("Illegal iteration: Spreader.flag")

            # 根据 n 的值替换表达式
            n = int(ns)
            if Spreader.flag == 1:
                s = Spreader.definitions_list[2 if n > 2 else n].replace("x", f'({param1})') \
                    .replace("n-1", str(n - 1)).replace("n-2", str(n - 2))
            elif Spreader.flag == 2:
                s = Spreader.definitions_list[2 if n > 2 else n].replace("y", f'({param2})') \
                    .replace("n-1", str(n - 1)).replace("n-2", str(n - 2))
            else:
                s = Spreader.definitions_list[2 if n > 2 else n].replace("x", f'({param1})').replace("y", f'({param2})') \
                    .replace("n-1", str(n - 1)).replace("n-2", str(n - 2))

            # 替换输入字符串中的函数调用
            input_str = input_str[:matcher.start()] + f'({s})' + input_str[pos + 1:]
            matcher = pattern.search(input_str)

        return input_str


def expand_expression(s, recursion_str, str0, str1):
    """
    基于给定的表达式展开 s
    :param s: 输入字符串，包含函数调用
    :param recursion_str: f{n}(x,y) 的递推表达式
    :param str0: f{0}(x,y) 的表达式
    :param str1: f{1}(x,y) 的表达式
    :return: 展开后的字符串
    """
    # 设置定义
    definitions = [str0, str1, recursion_str]
    Spreader.set_definition(definitions)

    # 展开 s
    result = Spreader.spread(s)
    return result

if __name__ == '__main__':
    res = expand_expression(s = "f{4} (((f{2}(	+1,  (cos 	((+		(x) 	+- (x 	^  4)^	0 	*-20	-	 (1))	 ) ^1)	 )	-f{4}(3603,		(- (1401 + (	+ -7	 )+f{4}( 	(x)	 ^	0,(x		^6)  )++3671	 +(	-x	*	 sin	(x)	 ^	0 )+  sin((9509) 	)^9	)	* 	+41	-((  +		(+8) )-		+		(+2) 	)-  ( +936 	) 	-x  )	 ) -	sin(cos(((sin(+209 	)	^	 9+x	*	(x^8) ^0- 	7244		+8-8989	 )) ^9	 )	 ^	0 	)^ 	8))^	6,	-58	)  ",\
recursion_str = "f{n}(	x ,	y) =2 * f{n - 1}	((	  -326) *71 * 04) - -8 * f{n - 2}( y )+	+ y	",\
str0 = "f{0}	(	 x ,	y)  =		+cos (+4	 )^ 3",\
str1 = "f{1}(x, y) = x ^ 9 - y")
    print(res)


