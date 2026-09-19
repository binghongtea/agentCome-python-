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

file_path = Path(__file__).resolve().parent / "test.png"
response = client.files.create(
    file=open(file_path, "rb"),
    purpose="user_data",
)

print(response)


