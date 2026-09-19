from openai import OpenAI
import os
# 从环境变量获取API密钥，配置方法见：https://www.volcengine.com/docs/82379/1399008
api_key = os.getenv('ARK_API_KEY')
# 初始化客户端，配置API地址与工具启用头
client = OpenAI(
    base_url='https://ark.cn-beijing.volces.com/api/v3',
    api_key=api_key,
    default_headers={"ark-beta-image-process": "true"}
)
# 发起图像处理请求
response = client.responses.create(
    model="doubao-seed-2-1-pro-260628",
    tools=[
        {
            "type": "image_process",
            "point": {
                "type": "disabled"
            },
            "grounding": {
                "type": "disabled"
            },
            "zoom": {
                "type": "enabled" # 启用缩放（zoom）工具
            },
            "rotate": {
                "type": "disabled"
            }
        }
    ],
    input=[
        {
            "type": "message",
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": "https://ark-project.tos-cn-beijing.volces.com/doc_image/image_process_1.jpg"  # 输入图片 URL
                },
                {
                    "type": "input_text",
                    "text": "前方路牌写了什么？"  # 系统提示文本
                }
            ]
        }
    ],
    stream=True  # 启用流式响应，实时获取处理结果
)
# 打印流式响应结果
for chunk in response:
    if hasattr(chunk, 'delta'):
        print(chunk.delta, end="", flush=True)