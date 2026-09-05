# -*- coding: utf-8 -*-
"""
19_9.5.py —— 极简版「模拟 GPT 逐字打印」模板
只用「生成器 + 迭代器」，模拟 ChatGPT 回答时一个字一个字蹦出来的打字机效果。

核心思路：
    生成器 (generator) 本身就是一种迭代器 (iterator)。
    函数里遇到 yield 就暂停并交出一个字符；for / next() 每取一次，
    函数就从暂停的那一行继续往下跑，直到下一次 yield。
"""
import sys
import time


def gpt_reply_stream(text, delay=0.08):
    """生成器：把一整段回答 text 一个字符一个字符地吐出来。"""
    for ch in text:           # 遍历整段文字
        time.sleep(delay)     # 假装在“思考/生成”，顺便控制打印速度
        yield ch              # 关键：每轮只交出一个字符，然后原地暂停


# ---------- 用法 1：for 循环消费（最常用） ----------
def demo_for():
    print("\n>>> 演示1：用 for 循环逐字打印")
    msg = "你好呀！这就是用生成器模拟的 GPT 逐字输出效果。"
    for ch in gpt_reply_stream(msg):
        print(ch,end='',flush=True)
        # sys.stdout.write(ch)  # 写入输出缓冲区
        # sys.stdout.flush()    # 立即刷新到屏幕 => 打字机效果
    print()


# ---------- 用法 2：手动 iter()/next() 消费 ----------
def demo_next():
    print("\n>>> 演示2：用 iter() / next() 手动取字符")
    it = iter(gpt_reply_stream("Iterators & Generators!", delay=0.02))
    while True:
        try:
            ch = next(it)     # 每调一次，生成器往下跑到下一个 yield
            sys.stdout.write(ch)
            sys.stdout.flush()
        except StopIteration: # 吐完了，生成器抛出 StopIteration
            break
    print()


if __name__ == "__main__":
    demo_for()
    demo_next()
