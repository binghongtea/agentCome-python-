import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

# jsonschema格式响应
load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
client=OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
)

class Step(BaseModel):
    step: str
    expression: str
class MathResponse(BaseModel):
    steps: list[Step]
    final_answer: str

response = client.chat.completions.parse(
    model="doubao-seed-2-1-pro-260628",
    messages=[
        {"role": "system", "content": "你是一个数学领域专家"},
        {"role": "user", "content": "你给将‘8/10=？’与'3+5=?'的解题步骤写出来"},
    ],
    response_format=MathResponse,
)

# print(response.model_dump_json(indent=2,ensure_ascii=False))
print(response.choices[0].message.parsed)
print('-----------------'*10)
print(response.choices[0].message.model_dump_json(indent=2,ensure_ascii=False))