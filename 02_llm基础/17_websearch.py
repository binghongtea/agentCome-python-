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

tools = [
    {
        "type": "web_search",
        "max_keyword": 2,
        "sources":["douyin"]
    }
]

response = client.responses.create(
    model="doubao-seed-2-1-pro-260628",
    input=[
        {"role": "user", "content": [
            {
                "type": "input_text",
                "text": "今天杭州的天气如何"
            }
        ]}
    ],
    tools=tools,
)

print(response.model_dump_json(indent=2,ensure_ascii=False))
# print(response)