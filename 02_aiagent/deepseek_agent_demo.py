# -*- coding: utf-8 -*-
"""
deepseek_agent_demo.py
============================================================
把知乎文章《从零开始搭建一个属于自己的Agent》(ReAct 范式) 的"思想流程"，
用 2026 年当前的 DeepSeek API「原生 Function Calling」重新实现。

旧实现(文章 2025-06) vs 新实现(本 Demo)
  旧: 手写 ReAct 提示词 + 硬匹配解析 "Action:/Action Input:/Observation:"
      缺点: 解析脆弱、只能单轮调用工具
  新: tools 参数声明工具 -> 模型返回【结构化】tool_calls
      -> 你的代码执行工具 -> 把结果以 tool 角色回传 -> 循环，直到模型给出最终答案
      优点: 不用解析文本、天然支持多轮工具调用

运行前提:
  1. 在 https://platform.deepseek.com 注册并创建 API Key（需充值）
  2. 设置环境变量: DEEPSEEK_API_KEY
  3. 安装 SDK:     python -m pip install openai

注意: 旧模型名 deepseek-chat / deepseek-reasoner 已于 2026-07-24 下线。
当前: deepseek-v4-flash = 原来 chat 的等价物(快/便宜)，
      deepseek-v4-pro   = 原 reasoner 的等价物(强推理, 思考模式需另配)。
如遇模型名报错，以官方文档为准: https://api-docs.deepseek.com
============================================================
"""

import ast
import json
import os
from datetime import date, datetime, timedelta

from openai import OpenAI

deepseekApi = '我的dsApiKey'
# ---------------- 0. 客户端配置 ----------------
client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY", deepseekApi),
    base_url="https://api.deepseek.com",  # OpenAI 兼容接口
)
MODEL = "deepseek-v4-flash"  # 便宜够用；可换 "deepseek-v4-pro"


# ---------------- 1. 工具实现（对应文章的"工具库"） ----------------
def check_python_syntax(source_code: str) -> str:
    """用 Python 内置 ast 检查语法，替代文章的 tree-sitter 方案（零额外依赖）"""
    try:
        ast.parse(source_code)
        return "语法检查通过：该 Python 代码没有语法错误。"
    except SyntaxError as e:
        # 注意: SyntaxError 记录列位置的是 offset（从1开始，可能为 None），没有 column 属性
        loc = f"第 {e.lineno} 行" + (f" 第 {e.offset} 列" if e.offset else "")
        return f"语法错误: {e.msg}（{loc}）"


def get_today() -> str:
    """返回今天的日期"""
    return date.today().isoformat()


def add_days(base_date: str, days: int) -> str:
    """把 base_date(YYYY-MM-DD) 加上 days 天，返回新日期"""
    d = datetime.strptime(base_date, "%Y-%m-%d").date()
    return (d + timedelta(days=days)).isoformat()


# ---------------- 2. 工具 Schema（让模型"认识"工具） ----------------
# 对应文章的文本式工具描述，但现在用标准 JSON Schema + 原生 tools 参数
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "check_python_syntax",
            "description": "检查一段 Python 源代码是否存在语法错误，返回错误位置和原因。",
            "parameters": {
                "type": "object",
                "properties": {
                    "source_code": {"type": "string", "description": "要检查的 Python 源代码"}
                },
                "required": ["source_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_today",
            "description": "获取今天的日期，格式 YYYY-MM-DD。当用户问'今天几号'这类问题时使用。",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_days",
            "description": "给定一个 YYYY-MM-DD 日期，加上指定天数，返回新日期。",
            "parameters": {
                "type": "object",
                "properties": {
                    "base_date": {"type": "string", "description": "起始日期 YYYY-MM-DD"},
                    "days": {"type": "integer", "description": "要加的天数"},
                },
                "required": ["base_date", "days"],
            },
        },
    },
]

# 工具名 -> 实现函数 的映射（对应文章的 call_plugin 分发）
TOOL_FUNCS = {
    "check_python_syntax": check_python_syntax,
    "get_today": get_today,
    "add_days": add_days,
}


# ---------------- 3. Agent 主循环（对应文章的 ReAct 流程） ----------------
def run_agent(user_question: str, max_rounds: int = 8) -> None:
    messages = [{"role": "user", "content": user_question}]
    print(f"[用户] {user_question}\n" + "=" * 60)

    for i in range(max_rounds):
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,          # 模型"看得到"的工具栏
            tool_choice="auto",   # auto=由模型决定是否调用
        )
        print(resp)
        print('*' * 100)
        msg = resp.choices[0].message

        # 情况 A：模型没有要调用工具 -> 这就是最终答案
        if not msg.tool_calls:
            print("[Agent 最终回答]\n" + (msg.content or ""))
            return

        # 情况 B：模型要调用工具 -> 执行并把结果回传
        # 注意1: 先把 assistant 这条(含 tool_calls)原样放回历史，否则 API 报错
        assistant_msg = {
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {
                    "id": c.id,
                    "type": "function",
                    "function": {"name": c.function.name, "arguments": c.function.arguments},
                }
                for c in msg.tool_calls
            ],
        }
        messages.append(assistant_msg)

        for call in msg.tool_calls:
            name = call.function.name
            args = json.loads(call.function.arguments or "{}")
            print(f"[第{i+1}轮 | 调用工具] {name}({args})")
            result = TOOL_FUNCS[name](**args)
            print(f"[工具返回] {result}")
            # 注意2: 工具结果用 role="tool" + tool_call_id 回传
            messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    print("[已达最大轮次，未得到最终答案]")


# ---------------- 4. 实战测试（对应文章的测试用例） ----------------
if __name__ == "__main__":
    # 用例 1：复刻文章的"修复 Python 语法错误"（验证：模型应调用 check_python_syntax）
    q1 = (
        "请修复下面 Python 代码中的语法错误，并输出修复后的完整代码：\n"
        "def hello_world():\n"
        "    print('Hello, World!')\n"
        "\n"
        "def hello_world2()::::\n"
        "    print('Hello, World2!')"
    )
    run_agent(q1)

    print("\n" + "#" * 60 + "\n")

    # 用例 2：需要【两次】工具调用的链式问题（验证：多轮循环 get_today -> add_days）
    run_agent("今天是几号？算一下 100 天之后的日期。")
