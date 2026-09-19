import os
from openai import OpenAI
from dotenv import load_dotenv
import json_repair

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
client=OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
)

prefix = "{"

response = client.chat.completions.create(
    model="doubao-seed-2-1-pro-260628",
    messages=[
        {"role": "user", "content": "帮我把豆包的基础架构用json格式输出。"},
        {"role":"assistant", "content": prefix}
    ]
)


# print(response.choices[0].message.content)
answer = prefix + response.choices[0].message.content
print('*'*100)

try:
    json.loads(answer)
    print('json.loads成功',answer)
except:
    json_repair.loads(answer)
    print('json.loads失败',answer)

# with response:
#     for chunk in response:
#         if chunk.choices[0].delta.content is not None:
#             print(chunk.choices[0].delta.content, end="")
