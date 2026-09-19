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
        {"role": "user", "content": "我先在要写一部小说，请你接着续写。韩立看到敌人如此强大，竟然隐藏的这么深，是一个元婴期强者，不禁眉头一皱，退至另外三位同行者的身后。"},
        {"role":"assistant", "content": "韩立:"}
    ]
)

if hasattr(response.choices[0].message, "reasoning_content"):
    print(response.choices[0].message.reasoning_content)

print('*'*100)
print(response.choices[0].message.content)

# with response:
#     for chunk in response:
#         if chunk.choices[0].delta.content is not None:
#             print(chunk.choices[0].delta.content, end="")
