# -*- coding: utf-8 -*-
"""
22_9.5fastapi.py —— FastAPI 入门 Demo（带详细注释）
================================================

【FastAPI 是什么】
    用 Python 写「Web 接口(API)」的框架：给每个网址绑定一个函数，
    别人通过 HTTP 访问你的网址时，函数就被执行、返回值作为响应发回对方。

【和你上一个文件(21_9.5.py)的关系】
    21_9.5.py 用 requests 去「调用别人的接口」 → 你是客户端(client)
    本文件 用 FastAPI 自己「提供接口给别人调」 → 你是服务端(server)
    两个都是 HTTP，一个是发请求的一方，一个是收请求的一方。

【第一次运行步骤】
    1) 安装（终端执行一次即可）：
           pip install fastapi uvicorn
    2) 运行本文件：
           python 22_9.5fastapi.py
    3) 浏览器打开：
           http://127.0.0.1:8000/       ← 接口1 hello
           http://127.0.0.1:8000/docs   ← FastAPI 白送的交互式文档(Swagger)
           http://127.0.0.1:8000/items/5?q=abc   ← 接口2（带参数）
    4) 想用 requests 调自己写的接口？开个新终端再跑一份 21_9.5.py 那种代码，
       把 url 改成 http://127.0.0.1:8000/ 就行 —— 你就打通了"客户端⇄服务端"

【为什么先学它】
    · 装饰器 + 普通函数 = 一个接口，不用手动处理网络底层
    · 类型注解自动变成「参数校验」，传错类型返回 422 而不是程序崩溃
    · 原生支持 async/await —— 和你刚学的 asyncio 语法完全一样
"""
import asyncio

from fastapi import FastAPI
from pydantic import BaseModel  # 用「类」定义数据格式，pydantic 负责自动校验

app = FastAPI(title="我的第一个 FastAPI 接口")  # app 就是整个后端服务


# ---------- 接口 1：最简 GET ----------
@app.get("/")
def hello():
    """浏览器访问 http://127.0.0.1:8000/ 时执行这个函数"""
    return {"message": "你好，FastAPI！"}  # 返回 dict 会自动转成 JSON


# ---------- 接口 2：路径参数 + 查询参数 ----------
@app.get("/items/{item_id}")
def get_item(item_id: int, q: str = "没有传"):
    """
    网址 /items/5 里的 5 自动传入 item_id
    网址 /items/5?q=abc 里的 abc 自动传入 q（q 不传就用默认值）
    注意 item_id: int —— 类型注解让 FastAPI 自动校验：
    访问 /items/abc 会返回 422 校验错误，而不是让程序内部崩溃
    """
    return {"item_id": item_id, "你查询的内容": q}


# ---------- 接口 3：POST + 请求体(Body) ----------
class User(BaseModel):
    """
    用「类」描述请求体(JSON)长什么样 —— 你学过的类 + pydantic 校验：
    - name 必填（没有默认值）
    - age / city 有默认值 => 前端可以不传
    收到的 JSON 会被自动转成 User 对象，字段不对会返回 422
    """
    name: str
    age: int = 0
    city: str = "未知"


@app.post("/users")
async def create_user(user: User):
    """POST 接收 JSON 请求体，模拟创建用户后返回结果"""
    await asyncio.sleep(0.2)  # 假装在异步处理业务 —— 语法和你学的 asyncio 一模一样
    return {
        "msg": f"欢迎 {user.name}！来自 {user.city}，今年 {user.age} 岁",
        "user": user,          # pydantic 对象也可以直接放进返回值
    }


# ---------- 启动 ----------
if __name__ == "__main__":
    import uvicorn
    # 启动开发服务器。浏览器或 requests 访问 http://127.0.0.1:8000
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="192.168.8.157", port=8080)
# 【延伸：不用浏览器调 POST 接口？】
#   打开 http://127.0.0.1:8000/docs 点 "Try it out" 即可；或终端 curl：
#   curl -X POST http://127.0.0.1:8000/users ^
#        -H "Content-Type: application/json" ^
#        -d "{\"name\":\"张三\",\"age\":18,\"city\":\"北京\"}"
