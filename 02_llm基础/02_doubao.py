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

response = client.responses.create(
    model="doubao-seed-2-1-pro-260628",
    input=[
        {"role": "user", "content": [
            {
                "type": "input_image",
                "image_url": "https://cdn.pixabay.com/photo/2026/09/09/03/21/pen_ash-crimson-rosella-10466152_1280.jpg"
            },
            {
                "type": "input_text",
                "text": "这图片有什么含义"
            }
        ]}
    ],
)

print(response.model_dump_json(indent=2,ensure_ascii=False))
# print(response)