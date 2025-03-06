#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
表达式等价比对器
用于判断两个数学表达式是否等价，通过调用大模型API进行判断
"""

import argparse
import sys
from http.client import responses

import requests
import json
import os


def parse_arguments(expr1, expr2, api, base_url, model):
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='判断两个数学表达式是否等价')

    # 必需参数：两个表达式
    parser.add_argument('--expr1', type=str,
                        default=expr1, help='第一个数学表达式')
    parser.add_argument('--expr2', type=str,
                        default=expr2, help='第二个数学表达式')

    # API相关参数
    parser.add_argument('--base_url', type=str,
                        default=base_url,
                        help='大模型API的基础URL (默认从环境变量LLM_API_BASE_URL获取，或使用OpenAI的URL)')
    print(f"api : {api}")
    parser.add_argument('--api_key', type=str,
                        default=api,
                        help='大模型API的密钥 (默认从环境变量LLM_API_KEY获取)')

    parser.add_argument('--model', type=str,
                        default=model,
                        help='使用的模型名称 (默认从环境变量LLM_MODEL获取，或使用gpt-3.5-turbo)')

    parser.add_argument('--temperature', type=float, default=0.0,
                        help='模型输出的随机性 (0-1之间，默认为0，表示最确定性的输出)')

    parser.add_argument('--verbose', action='store_true',
                        help='启用详细输出模式，显示API请求和响应的详细信息')

    return parser.parse_args()


def generate_prompt(expr1, expr2):
    """
    根据两个表达式生成提示文本

    Args:
        expr1 (str): 第一个数学表达式
        expr2 (str): 第二个数学表达式

    Returns:
        list: 包含系统提示和用户提示的消息列表
    """
    system_message = {
        "role": "system",
        "content": "你是一个专业的数学表达式分析工具。你的任务是判断两个数学表达式是否等价。"
                   "请只回答'等价'或'不等价'，不要有任何其他解释。"
    }

    user_message = {
        "role": "user",
        "content": f"请判断以下两个数学表达式是否等价：\n表达式1: {expr1}\n表达式2: {expr2}\n"
                   f"如果它们在所有可能的取值下都相等，则回答'等价'，否则回答'不等价'。"
                   f"请只回答'等价'或'不等价'，不要有任何解释。"
    }

    return [system_message, user_message]


def call_llm_api(base_url, api_key, model, messages, temperature=0.0):
    """
    调用大模型API

    Args:
        base_url (str): API基础URL
        api_key (str): API密钥
        model (str): 模型名称
        messages (list): 消息列表
        temperature (float): 温度参数，控制随机性

    Returns:
        str: 模型的回复文本

    Raises:
        Exception: 当API调用失败时抛出异常
    """
    # 构建完整的API URL
    api_url = f"{base_url.rstrip('/')}/chat/completions"

    # 设置请求头
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # 构建请求体
    data = {
        "model": model,
        "messages": messages,
        "temperature": temperature
    }

    try:
        # 发送POST请求
        response = requests.post(api_url, headers=headers, data=json.dumps(data), timeout=30)

        # 检查响应状态
        response.raise_for_status()

        # 解析JSON响应
        result = response.json()

        # 提取模型回复的文本
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"].strip()
        else:
            raise Exception("API响应中未找到有效的回复内容")

    except requests.exceptions.RequestException as e:
        raise Exception(f"API请求失败: {str(e)}")
    except json.JSONDecodeError:
        raise Exception("无法解析API响应的JSON数据")
    except Exception as e:
        raise Exception(f"调用API时发生错误: {str(e)}")


def parse_equivalence_result(response_text):
    """
    解析API响应，判断表达式是否等价

    Args:
        response_text (str): API返回的文本

    Returns:
        tuple: (是否等价的布尔值, 原始响应文本)
    """
    # 转换为小写并去除空白字符，便于匹配
    normalized_text = response_text.lower().strip()

    # 判断是否包含"等价"关键词
    if "等价" in normalized_text and "不等价" not in normalized_text:
        return True, response_text
    # 判断是否包含"不等价"关键词
    elif "不等价" in normalized_text:
        return False, response_text
    # 英文关键词判断（兼容英文回复）
    elif "equivalent" in normalized_text and "not equivalent" not in normalized_text:
        return True, response_text
    elif "not equivalent" in normalized_text:
        return False, response_text
    else:
        # 无法确定结果
        return None, response_text


def ai_test_equivalent(expr1, expr2, api, base_url, model):
    """主函数"""
    # 解析命令行参数
    args = parse_arguments(expr1, expr2, api, base_url, model)

    # 检查API密钥是否提供
    if not args.api_key:
        print("错误：未提供API密钥。请使用--api_key参数或设置LLM_API_KEY环境变量。")
        sys.exit(1)

    # 生成提示
    messages = generate_prompt(args.expr1, args.expr2)

    # 详细模式下显示提示信息
    if args.verbose:
        print("\n生成的提示:")
        for msg in messages:
            print(f"{msg['role']}: {msg['content']}")

    try:
        # 调用大模型API
        print(f"\n正在调用API判断表达式是否等价...")
        print(args)
        response_text = call_llm_api(
            args.base_url,
            args.api_key,
            args.model,
            messages,
            args.temperature
        )

        # 详细模式下显示原始响应
        if args.verbose:
            print(f"API原始响应: {response_text}")

        # 解析结果
        is_equivalent, raw_response = parse_equivalence_result(response_text)

        # 输出结果
        print("\n判断结果:")
        print(f"表达式1: {args.expr1}")
        print(f"表达式2: {args.expr2}")

        if is_equivalent is True:
            print("结论: 等价 ✓")
            return 0  # 返回成功状态码
        elif is_equivalent is False:
            print("结论: 不等价 ✗")
            return 1  # 返回失败状态码
        else:
            print(f"结论: 无法确定 (?)")
            print(f"原始响应: {raw_response}")
            print("提示: API返回的内容不包含明确的'等价'或'不等价'关键词")
            return 2  # 返回未知状态码

    except Exception as e:
        print(f"错误: {str(e)}")
        return 3  # 返回错误状态码


if __name__ == "__main__":
    sys.exit(ai_test_equivalent())