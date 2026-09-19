import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
print(API_KEY)

client=OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
)

conversation_list = [
    {"role": "system", "content": "你是一个十进制内的计算专家"}
]


def get_response(user_input):
    conversation_list.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="doubao-seed-2-1-pro-260628",
        messages=conversation_list,
    )
    conversation_list.append({"role": "assistant", "content": response.choices[0].message.content})
    return response.choices[0].message.content

print(f"第一次请求：{get_response("1加1等于几")}")
print(f"第二次请求：{get_response("再加3")}")
print(f"第三次请求：{get_response("再加4")}")
print(f"第四次请求：{get_response("再加5")}")
# print(response.model_dump_json(indent=2,ensure_ascii=False))
# print(response.choices[0].message.content)