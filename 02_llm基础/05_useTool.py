import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
client=OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
)

tools = [
    {
        "type": "function",
        "description": "查询城市的天气",
        "function": {
            "name": "get_weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    },
                    "unit": {
                        "type": "string",
                        "description": "温度单位，默认摄氏度"
                    }
                },
                "required": ["city", "unit"],
            }
        }
    }
]

# 定义工具函数，正常是调个api
def get_weather(city, unit="celsius"):
    return f"{city}的天气是晴朗{unit}25"


messages_list = [
    {"role": "system", "content": ""},
    {"role": "user", "content": "上海和北京今天天气怎么样？"}
]

while True:
    response = client.chat.completions.create(
        model="doubao-seed-2-1-pro-260628",
        messages=messages_list,
        tools=tools
    )
    print(response.choices[0].message.model_dump_json(indent=2,ensure_ascii=False))
    if response.choices[0].finish_reason != "tool_calls":
        break
    messages_list.append(response.choices[0].message.model_dump())
    tool_calls = response.choices[0].message.tool_calls
    for tool_call in tool_calls:
        args = tool_call.function.arguments
        args = json.loads(args)
        tool_result = get_weather(**args)
        messages_list.append({"role": "tool", "content": tool_result, "tool_call_id": tool_call.id})

while True:
    response = client.chat.completions.create(
        model="doubao-seed-2-1-pro-260628",
        messages=messages_list,
        tools=tools
    )
    print(response.choices[0].message.model_dump_json(indent=2,ensure_ascii=False))
    if response.choices[0].finish_reason != "tool_calls":
        print(response.choices[0].message.content)
        break


print(messages_list.model_dump_json(indent=2,ensure_ascii=False))
