import os
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
client = OpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
)


print(client.files.list().model_dump_json(indent=2, ensure_ascii=False))


