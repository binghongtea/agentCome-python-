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
        {"role": "system", "content": "在回答最后加个笑脸"},
        {"role": "user", "content": "二月有几天"}
    ],
    reasoning_effort= "medium",
)

if hasattr(response.choices[0].message, "reasoning_content"):
    print(response.choices[0].message.reasoning_content)
print(response.choices[0].message.content)

# with response:
#     for chunk in response:
#         if chunk.choices[0].delta.content is not None:
#             print(chunk.choices[0].delta.content, end="")
