import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
client=OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
)

response = client.chat.completions.create(
    model="doubao-seed-2-1-pro-260628",
    messages=[
        {"role": "system", "content": "你是一个十进制内的计算专家"},
        {"role": "user", "content": "1加1等于几"},
        {"role": "assistant", "content": "2"},
        {"role": "user", "content": "在加3"},
        {"role": "assistant", "content": "5"},
        {"role": "user", "content": "在加4"},
    ],
    extra_body={"thinking": {"type": "enabled"}},
)

# print(response.model_dump_json(indent=2,ensure_ascii=False))
print(response.choices[0].message.content)