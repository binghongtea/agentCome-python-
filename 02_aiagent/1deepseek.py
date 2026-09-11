import os
from openai import OpenAI

os.environ['OPENAI_API_KEY'] = ''

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {"role": "user", "content": "你好"},
        {"role": "assistant", "content": "你好！我是DeepSeek的助手。"},
    ],
    stream=False,
    reasoning_effort='medium',
    extra_body={
        "thinking": {"type": "enabled"}
    }
)

print(response.model_dump_json(indent=2,ensure_ascii=False))
print(response.choices[0].message.content)