import asyncio
import base64
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

API_KEY = os.getenv("ARK_API_KEY")
client = AsyncOpenAI(
    base_url="https://ark.cn-beijing.volces.com/api/v3",
    api_key=API_KEY,
)

def image_to_data_url(file_path: str | Path) -> str:
    """把本地图片转成 base64 data URI，mime 按扩展名推断"""
    suffix = Path(file_path).suffix.lower().lstrip(".")
    mime = {
        "png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
        "webp": "image/webp", "gif": "image/gif", "bmp": "image/bmp",
    }.get(suffix)
    if mime is None:
        raise ValueError(f"无法识别图片扩展名：{suffix}")
    with open(file_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


async def main():
    file_path = Path(__file__).resolve().parent / "test.png"
    image_url = image_to_data_url(file_path)
    response = await client.responses.create(
        model="doubao-seed-2-1-pro-260628",
        input=[
            {
                "role": "user",
                "content": [
                    {"type": "input_image", "image_url": image_url},
                    {"type": "input_text", "text": "这图片有什么含义"},
                ],
            }
        ],
    )
    print(response.output_text)
    print("-" * 170)

if __name__ == "__main__":
    asyncio.run(main())
